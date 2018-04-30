from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api_v0.serializers import ProfileSerializer, NotificationSerializer, ExaminationSerializer
from core import helpers
from core.helpers import send_email_with_security_code
from core.models import *


def sign_in(request):
    if request.user.is_active:
        return HttpResponseRedirect("/")
    else:
        return render(request, 'core/sign_in.html', {})


def login_view(request):
    username = request.POST['login']
    password = request.POST['pass']
    user = authenticate(username=username, password=password)
    if not request.POST.get('remember-me'):
        request.session.set_expiry(0)
    if user is not None:
        if user.is_active:
            login(request, user)
            if ('next' in request.GET):
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect("/")
        else:
            messages.add_message(request, messages.INFO, "аккаунт недоступен")
            return HttpResponseRedirect(reverse('core:sign-in'))
    else:
        messages.add_message(request, messages.INFO, "некорректный логин или пароль")
        return HttpResponseRedirect(reverse('core:sign-in'))

@login_required(login_url='/sign-in')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("core:sign-in"))

@login_required(login_url='/sign-in')
@api_view(['GET'])
def main(request):
    user = request.user
    last_notifications = Notification.objects.filter(user=user).order_by('-date_time')[:2]
    last_examinatinos = Examination.objects.filter(doctor=user).order_by('-date_time')[:2]
    #notifications_amount = Notification.objects.filter(user=user).count()

    notifs_serializer = NotificationSerializer(last_notifications, many=True)
    notifs_data = notifs_serializer.data

    exams_serializer = ExaminationSerializer(last_examinatinos, many=True)
    exams_data = exams_serializer.data

    data = [
        notifs_data,
        exams_data
    ]

    return Response(data)

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
@api_view(['POST'])
def save_examination(request, pk):
    helpers.calc_probability(pk=pk, doctor=request.user,
                             patient="", )  # sym=request.data["symptoms"], analysis=request.data["analysis"]
    examination = Examination.objects.get(pk=pk)
    serializer = ExaminationSerializer(examination)
    return Response(serializer.data)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        send_email_with_security_code(email)
        logout(request)
        return HttpResponseRedirect(reverse('core:forgot-password'))


def insert_to_database(request):
    filename = ""
    file = open(filename, encoding="UTF-8")
    for line in file:
        disease = Disease()
        pk, name = line.split(",", 1)
        print(pk, name.lower().strip())
        disease.pk = int(pk.strip())
        disease.name = name.lower().strip()
        disease.save()
    print("--")
    return HttpResponse("OK" + str(Disease.objects.count()))


def insert_connections(request):
    filename = ""
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
