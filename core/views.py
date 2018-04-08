from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from core.helpers import send_email_with_security_code
from core.models import Notification


def sign_in(request):
    if request.user.is_active:
        return HttpResponseRedirect(reverse('core:main'))
    else:
        return render(request, 'core/sign_in.html', {})


def login_view(request):
    username = request.POST['login']
    password = request.POST['pass']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            if ('next' in request.GET):
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse("core:main"))
        else:
            messages.add_message(request, messages.INFO, "disabled account")
            return HttpResponseRedirect(reverse('core:sign-in'))
    else:
        messages.add_message(request, messages.INFO, "invalid login or password")
        return HttpResponseRedirect(reverse('core:sign-in'))

@login_required(login_url='/sign-in')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("core:sign-in"))



@login_required(login_url='/sign-in')
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def main(request):
    user = request.user

    notifications_amount = Notification.objects.filter(user=user).count()

    return Response({})

@login_required(login_url='/sign-in')
@api_view(['GET'])
def profile(request):
    return Response({})


@login_required(login_url='/sign-in')
@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def notifications(request):
    user = request.user
    notifs = Notification.objects.filter(user=user)
    serializer = Notification(instance=notifs)
    data = serializer.data
    return Response(data, template_name='core/notifications.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        send_email_with_security_code(email)
        logout_view(request)
        return HttpResponseRedirect(reverse('core:forgot-password'))
    else:
        return render(request, 'core/forgot-password.html', {})




