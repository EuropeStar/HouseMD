from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.urls import reverse

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
