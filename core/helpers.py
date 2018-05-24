import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.naive_bayes import BernoulliNB

from core.models import Symptom, Disease, Examination, DiseaseProbability, AnalysisParams, AnalysisConstants, \
    DiseaseAnalysis

# from core.models import Disease, Symptom

fromaddr = "vladislav.itis@gmail.com"
mypass = "*********"


def send_email(toaddr, message):
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "House MD"
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, mypass)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def send_email_with_security_code(toaddr):
    message = str(random.randint(1000, 10000))
    send_email(toaddr, message)


def normalize(diseases: list) -> list:
    """    
    This function normalized list with probability item
    :param diseases: list of list, first item is disease`s name, second item is probability, third item is number of symptoms
    :return: list with normalized probability item 
    """
    summ = sum([d[1] for d in diseases])
    for d in diseases:
        if summ != 0:
            d[1] = d[1] * (1 / summ)
        else:
            d[1] = 1 / len(diseases)
    return diseases


def prepare_dis_vector(diseases_array: list, symptoms_array: list) -> list:
    """
    This function calculate list with probability item
    :param diseases_array: list of Disease items
    :param symptoms_array: list of Symptom items
    :return: list with probability item
    """
    dis = []
    for d in diseases_array:
        try:
            prob = Examination.objects.filter(diseases__disease=d).count() / Examination.objects.all().count()
        except ZeroDivisionError:
            prob = 0

        dis.append([d.name, prob,
                    len(d.symptoms.intersection(symptoms_array)) / len(symptoms_array)])

    return normalize(dis)


def calc_symptoms_diseases_matrix(diseases_array: list, symptoms_array: list) -> list:
    """
    This function calculate inverted correlation matrix
    :param diseases_array: list of Disease items
    :param symptoms_array: list of Symptom items
    :return: matrix of probabilities
    """
    p_symptoms_diseases = []
    for i in range(len(diseases_array)):
        p_symptoms_diseases.append([])
        line = p_symptoms_diseases[i]
        for j in range(len(symptoms_array)):
            try:
                prob = Examination.objects.filter(diseases__disease__name=diseases_array[i].name,
                                                  symptoms__name=symptoms_array[
                                                      j].name).count() / Examination.objects.all().count()
            except ZeroDivisionError:
                prob = 0
            line.append(prob)
    return p_symptoms_diseases


def calc_invert_symptoms_diseases_matrix(diseases_array: list, symptoms_array: list,
                                         dis: list, sym: list, p_symptoms_diseases: list) -> list:
    """
    This function calculate correlation matrix
    :param diseases_array: list of Disease items
    :param symptoms_array: list of Symptom items
    :param dis: list of list, first item is disease`s name, second item is probability, third item is number of symptoms
    :param sym: list of symptom`s name
    :param p_symptoms_diseases: matrix of symptoms frequency for every diseases 
    :return: matrix of inverted probabilities
    """
    p_symptoms_not_diseases = [[0] * len(symptoms_array) for i in range(len(diseases_array))]
    for i in range(len(dis)):
        for j in range(len(sym)):
            summ = 0
            for k in range(len(dis)):
                if k != i:
                    summ += p_symptoms_diseases[k][j]
            try:
                p_symptoms_not_diseases[i][j] = summ / (len(dis) - 1)
            except  ZeroDivisionError:
                p_symptoms_not_diseases[i][j] = summ
    return p_symptoms_not_diseases


def bayes_probability(dis: list, sym: list, p_symptoms_diseases: list, p_symptoms_not_diseases: list) -> list:
    """
    This function calculate Bayesian probabilities
    :param dis: list of list, first item is disease`s name, second item is probability, third item is number of symptoms
    :param sym: list of symptom`s name
    :param p_symptoms_diseases: matrix of symptoms frequency for every diseases 
    :param p_symptoms_not_diseases: matrix of symptoms frequency for set diseases excluding fixed one
    :return: modified dis
    """
    for i in range(len(dis)):
        for j in range(len(sym)):
            p_s_d = p_symptoms_diseases[i][j]
            p_d = dis[i][1]
            p_s_not_d = p_symptoms_not_diseases[i][j]
            p_d_s = 0
            if (p_s_d * p_d + p_s_not_d * (1 - p_d)) != 0:
                p_d_s = p_s_d * p_d / (p_s_d * p_d + p_s_not_d * (1 - p_d))
            dis[i][1] = p_d_s
    return dis


def calc_probability(doctor, sex, age, patient: str, sym: list = [], analysis: list = [], pk=None) -> int:
    """
    This function calculate probabilities od diseases and check analysis values 
    :param doctor: instance of type User: 
    :param sex: id param of patient`s sex
    :param age:  id param of patient`s age
    :param sym:  list of symptoms id, default []
    :param analysis: list of analysis id, default []
    :param patient: fullname of patient
    :param pk: pk param of existed examination, default None
    :return pk of modified Examination instance: 
    """
    if pk:
        examination = Examination.objects.get(pk=pk)
        examination.doctor = doctor
        examination.patient = patient
        examination.sex = sex
        examination.age = age
    else:
        examination = Examination(doctor=doctor, patient=patient,
                                  age=age,
                                  sex=sex)
    examination.save()
    examination.symptoms.clear()
    examination.diseases.all().delete()
    examination.diseases.clear()
    sym = list(filter(lambda elem: elem != '', sym))
    symptoms_array = Symptom.objects.filter(id__in=sym)
    examination.symptoms.add(*symptoms_array)
    diseases_array = Disease.objects.filter(symptoms__in=symptoms_array).order_by("name")
    # .filter(len(F("symptoms")) > int(len(sym) * 0.75))

    dis = prepare_dis_vector(diseases_array, symptoms_array)

    p_symptoms_diseases = calc_symptoms_diseases_matrix(diseases_array, symptoms_array)
    # for row in p_symptoms_diseases:
    #     row.sort(key=lambda x: x, reverse=True)
    p_symptoms_not_diseases = calc_invert_symptoms_diseases_matrix(diseases_array, symptoms_array, dis, sym,
                                                                   p_symptoms_diseases)
    dis = bayes_probability(dis, sym, p_symptoms_diseases, p_symptoms_not_diseases)
    dis = normalize(dis)

    for an in analysis:
        analysis_template = AnalysisConstants.objects.get(id=an["id"])
        scope = float(analysis_template.upper_bound - analysis_template.lower_bound)
        value = float(an["value"])
        if analysis_template.lower_bound <= value <= analysis_template.upper_bound:
            deviation = 0
        elif value <= analysis_template.upper_bound:
            deviation = - (float(analysis_template.lower_bound) - value) / scope
        else:
            deviation = (float(analysis_template.upper_bound) - value) / scope
        analysis_record = AnalysisParams(name=analysis_template, value=value, deviation=deviation,
                                         result=deviation != 0)
        analysis_record.save()

        examination.analysis.add(analysis_record)

    for i in range(len(dis)):
        disease_prob = DiseaseProbability(disease=diseases_array[i], prob=round(dis[i][1], 2))
        for an in examination.analysis.all().filter(result=True):
            dis_an = DiseaseAnalysis.objects.get(disease=diseases_array[i], analysis=an)
            if dis_an == None:
                continue
            sign = dis_an.sign
            if ((an.deviation > 0 and sign in (">", "<>")) or
                    (an.deviation < 0 and sign in ("<", "<>"))):
                disease_prob.analysis_result.add(an)
        disease_prob.save()
        examination.diseases.add(disease_prob)

    examination.save()
    return examination.pk


def create_dataset(filename):
    file = open(filename, "w", encoding="UTF-8")

    symptoms = Symptom.objects.all()
    diseases = Disease.objects.all()
    matrix = calc_symptoms_diseases_matrix(diseases, symptoms)
    file.write(','.join(str(sym.id) for sym in symptoms))
    file.write("\n")
    for i in range(len(matrix)):
        file.write(','.join(map(str, matrix[i])) + ',' + str(diseases[i].id) + '\n')
    file.close()


def readData(filename):
    dataset = pd.read_csv(filename, usecols=[0, 1], encoding='UTF-8')[1:]
    dataset.columns = ['content', 'label']
    return dataset


def learn(train_set):
    n = train_set.shape[0]
    m = 71
    X = np.zeros((n, m))
    for i in range(n):
        X[i, :] = train_set.iloc[i].content
    Y = train_set.label
    model = BernoulliNB()
    model.fit(X, Y)

    Y_hat = model.predict(X)
    accuracy = metrics.accuracy_score(Y, Y_hat)
    print('Accuarcy: {}'.format(accuracy))
    return model


def predict(lst, model):
    X = lst
    Y_hat = model.predict(X.reshape(1, -1))
    print(Y_hat, lst)
