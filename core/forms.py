from django import forms
from django.contrib.auth.models import User
from django.forms import modelformset_factory

from core.models import Profile, Examination


class AddUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    patronymic = forms.CharField(max_length=50)
    image = forms.ImageField()

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'patronymic', 'organisation', 'specialization', 'is_chief', 'image']


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    patronymic = forms.CharField(max_length=50)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'patronymic', 'specialization', 'is_chief']


class ChangeProfileForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    patronymic = forms.CharField(max_length=50)
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password_confirm = forms.CharField(widget=forms.PasswordInput)


class SignInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']


class ResearchForm(forms.ModelForm):
    class Meta:
        model = Examination
        fields = ['patient', 'age', 'sex', 'symptoms', 'contraindications', 'diseases', 'meds']


ProfileFormSet = modelformset_factory(form=ProfileForm, model=Profile, fields=ProfileForm.Meta.fields)
