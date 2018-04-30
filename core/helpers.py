import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from core.models import Symptom, Disease, Examination, DiseaseProbability

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


def normalize(diseases: list):
    summ = sum([d[1] for d in diseases])
    for d in diseases:
        if summ != 0:
            d[1] = d[1] * (1 / summ)
    return diseases


def prepare_dis_vector(diseases_array, symptoms_array):
    dis = []
    for d in diseases_array:
        try:
            prob = Examination.objects.filter(diseases__disease=d).count() / Examination.objects.all().count()
        except ZeroDivisionError:
            prob = 0

        dis.append([d.name, prob,
                    len(d.symptoms.intersection(symptoms_array)) / len(symptoms_array)])

    # dis = list(filter(lambda x: x[2] > (len(symptoms_array) * 0.75), dis))

    return normalize(dis)

def calc_symptoms_diseases_matrix(diseases_array, symptoms_array):
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
    print(p_symptoms_diseases)
    return p_symptoms_diseases

def calc_invert_symptoms_diseases_matrix(diseases_array, symptoms_array, dis, sym, p_symptoms_diseases):
    p_symptoms_not_diseases = [[0] * len(symptoms_array) for i in range(len(diseases_array))]
    for i in range(len(dis)):
        for j in range(len(sym)):
            summ = 0
            for k in range(len(dis)):
                if k != i:
                    summ += p_symptoms_diseases[k][j]

            p_symptoms_not_diseases[i][j] = summ / (len(dis) - 1)
    print(p_symptoms_not_diseases)
    return p_symptoms_not_diseases

def bayes_probability(dis, sym, p_symptoms_diseases, p_symptoms_not_diseases):
    """
    p_s_d: "cимптом s при условии заболевания d"
    p_d: "заболевание d (без уточнения)"
    p_s_not_d: "cимптом s при условии заболевания не d"
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


def calc_probability(doctor, sym: list = None, analysis: list = None, pk=1, patient=""):
    examination, created = Examination.objects.get_or_create(pk=pk, doctor=doctor, patient=patient,
                                                             age=Examination.LESS_ZERO_AGE, sex=Examination.MALE)
    examination.symptoms.clear()
    examination.diseases.all().delete()
    examination.diseases.clear()

    symptoms_array = Symptom.objects.filter(name__in=sym)
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

    for i in range(len(dis)):
        disease_prob = DiseaseProbability(disease=diseases_array[i], prob=round(dis[i][1], 2))
        disease_prob.save()
        examination.diseases.add(disease_prob)
    examination.save()