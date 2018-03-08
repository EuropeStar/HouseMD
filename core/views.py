from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from core.helpers import send_email_with_security_code


def sign_in(request):
    if request.user.is_active:
        return redirect("/main/")
    else:
        return render(request, 'core/sign_in.html', {})


def login_view(request):
    username = request.POST['login']
    password = request.POST['pass']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect("/main/")
        else:
            messages.add_message(request, messages.INFO, "disabled account")
            return redirect('/sign-in/')
    else:
        messages.add_message(request, messages.INFO, "invalid login")
        return redirect('/sign-in/')

@login_required(login_url='/sign-in/')
def logout_view(request):
    logout(request)
    return redirect("/sign-in/")


@login_required(login_url='/sign-in/')
def main(request):
    return HttpResponse(request.user.username)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        send_email_with_security_code(email)
        logout(request)
        return redirect('/forgot-password/')
    else:
        return render(request, 'core/forgot-password.html', {})
