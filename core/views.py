from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from api_v0.serializers import ProfileSerializer, ExaminationSerializer
from core.helpers import send_email_with_security_code
from core.models import *
from core.helpers import send_email_with_security_code
from core.models import *



def sign_in(request):
    if request.user.is_active:
        return HttpResponseRedirect("/")
    else:
        return render(request, 'core/sign_in.html', {})

def insert_to_database(request):
    filename = r"C:\Users\vladi\PycharmProjects\cybermedics\HouseMD\symptoms-id.txt"
    file = open(filename, encoding="UTF-8")
    for line in file:
        symptom = Symptom()
        pk, name = line.split(",", 1)
        print(pk, name.lower().strip())
        symptom.pk = int(pk.strip())
        symptom.name = name.lower().strip()
        symptom.save()
    print("--")
    return HttpResponse("OK" + str(Symptom.objects.count()))

def insert_connections(request):
    filename = r"C:\Users\vladi\PycharmProjects\cybermedics\HouseMD\disease-symptoms.txt"
    file = open(filename, encoding="UTF-8")
    for line in file:
        l = line.strip().replace("]", "").replace("[", "").replace("-", "").replace(" ", "")
        a_id, b_array = l.split(",", 1)
        a_id = int(a_id)
        b_array = list(map(int, b_array.split(",")))
        print(a_id, b_array)
        dis = Disease.objects.get(pk=a_id)
        for id in b_array:
            sym = Symptom.objects.get(pk=id)
            dis.symptoms.add(sym)
    return HttpResponse("OK" + str(Symptom.objects.count()))

  
@login_required(login_url='/sign-in')
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def personal_administration(request):
    profiles = Profile.objects.all()
    profiles_serializer = ProfileSerializer(profiles, many=True)
    data = profiles_serializer.data
    return Response(data, template_name='core/personal_administration.html')


@login_required(login_url='/sign-in')
@api_view(['GET'])
def profile(request):
    profile = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(profile)
    profile_data = serializer.data
    return Response(profile_data)


@login_required(login_url='/sign-in')
@api_view(['GET'])
def notifications(request):
    user = request.user
    notifs = Notification.objects.filter(user=user)
    serializer = NotificationSerializer(notifs, many=True)
    return Response(serializer.data)

@login_required(login_url='/sign-in')
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def history(request):
    user = request.user
    examinations = Examination.objects.filter(doctor=user).order_by('-date_time')[:10]
    examination_serializer = ExaminationSerializer(examinations, many=True)
    data = examination_serializer.data
    return Response(data, template_name='core/history.html')


@login_required(login_url='/sign-in')
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def confirmation(request, examination_id):
    examination = Examination.objects.get(pk=examination_id)
    examination_serializer = ExaminationSerializer(examination)
    data = examination_serializer.data
    return Response(data, template_name='core/confirmation.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        send_email_with_security_code(email)
        logout(request)
        return HttpResponseRedirect(reverse('core:forgot-password'))


def insert_to_database(request):
    filename = r"C:\Users\vladi\PycharmProjects\cybermedics\HouseMD\symptoms-id.txt"
    file = open(filename, encoding="UTF-8")
    for line in file:
        symptom = Symptom()
        pk, name = line.split(",", 1)
        print(pk, name.lower().strip())
        symptom.pk = int(pk.strip())
        symptom.name = name.lower().strip()
        symptom.save()
    print("--")
    return HttpResponse("OK" + str(Symptom.objects.count()))


def insert_connections(request):
    filename = r"C:\Users\vladi\PycharmProjects\cybermedics\HouseMD\disease-symptoms.txt"
    file = open(filename, encoding="UTF-8")
    for line in file:
        l = line.strip().replace("]", "").replace("[", "").replace("-", "").replace(" ", "")
        a_id, b_array = l.split(",", 1)
        a_id = int(a_id)
        b_array = list(map(int, b_array.split(",")))
        print(a_id, b_array)
        dis = Disease.objects.get(pk=a_id)
        for id in b_array:
            sym = Symptom.objects.get(pk=id)
            dis.symptoms.add(sym)
    return HttpResponse("OK" + str(Symptom.objects.count()))
