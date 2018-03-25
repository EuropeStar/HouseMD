import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
        d[1] = d[1] * (1 / summ)
    return diseases


def calc_probability(diseases: list = None, symptoms: list = None) -> list:
    symptoms = ['кашель', 'насморк', 'головная боль']  # x
    diseases = [['Грипп', 0.2, 3], ['ОРЗ', 0.25, 3], ['Назофарингит', 0.35, 3], ['Гипертония', 0.1, 1]]  # y
    diseases = list(filter(lambda x: x[2] > (len(symptoms) * 0.75), diseases))
    diseases = normalize(diseases)
    p_symptoms_diseases = [
        [0.9, 0.7, 0.9],
        [0.5, 1, 0.9],
        [0.6, 1, 0.2],
        [0, 0, 1],
        # [1, 1, 1],
    ]

    for row in p_symptoms_diseases:
        row.sort(key=lambda x: x, reverse=True)

    p_symptoms_not_diseases = [[0] * len(symptoms) for i in range(len(diseases))]

    for i in range(len(diseases)):
        for j in range(len(symptoms)):
            summ = 0
            for k in range(len(diseases)):
                if k != i:
                    summ += p_symptoms_diseases[k][j]

            p_symptoms_not_diseases[i][j] = summ / (len(diseases) - 1)

    p_s_d: "cимптом s при условии заболевания d"
    p_d: "заболевание d (без уточнения)"
    p_s_not_d: "cимптом s при условии заболевания не d"

    for i in range(len(diseases)):
        for j in range(len(symptoms)):
            p_s_d = p_symptoms_diseases[i][j]
            p_d = diseases[i][1]
            p_s_not_d = p_symptoms_not_diseases[i][j]
            p_d_s = p_s_d * p_d / (p_s_d * p_d + p_s_not_d * (1 - p_d))
            diseases[i][1] = p_d_s
    return normalize(diseases)


if __name__ == "__main__":
    result = calc_probability()
    result.sort(key=lambda x: x[1], reverse=True)
    print(result)
    result = list(filter(lambda x: x[1] >= 0.2, result))
    print(result)
