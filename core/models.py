from typing import Tuple

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ActiveSubstance(models.Model):
    name = models.CharField(max_length=100, verbose_name="название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "aктивное вещество"
        verbose_name_plural = "активные вещества"


class SideEffect(models.Model):
    name = models.CharField(max_length=100, verbose_name="название")
    description = models.TextField(verbose_name="описание", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "побочный эффект"
        verbose_name_plural = "побочные эффекты"


class Med(models.Model):
    DOSE = (
        ()
    )
    name = models.CharField(max_length=100, verbose_name="название")
    description = models.TextField(verbose_name="описание", blank=True)
    category = models.CharField(max_length=100, blank=True, verbose_name="класс принадлежности")
    default_dose = models.CharField(max_length=100, blank=True, verbose_name="способ применения и дозы")
    efficiency_class = models.IntegerField(null=True, blank=True, verbose_name="класс эффективности")
    activeSubstances = models.ManyToManyField(ActiveSubstance, related_name='meds', verbose_name='активные вещества')
    side_effects = models.ManyToManyField(SideEffect, related_name='meds', verbose_name='побочные эффекты')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "препарат"
        verbose_name_plural = "препараты"


class Symptom(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "симптом"
        verbose_name_plural = "симптомы"


class Disease(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(verbose_name='описание', blank=True)
    counter = models.IntegerField(default=0)
    meds = models.ManyToManyField(Med, related_name='diseases', verbose_name='используемые препараты')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "заболевание"
        verbose_name_plural = "заболевания"


class Contraindication(models.Model):
    name = models.ForeignKey(ActiveSubstance, related_name='contraindications', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "противопоказание"
        verbose_name_plural = "противопоказания"


class SpringSymptDisease(models.Model):
    disease = models.ManyToManyField(Disease, related_name='spring_sympt_disease')
    symptom = models.ManyToManyField(Symptom, related_name='spring_sympt_disease')
    counter = models.IntegerField(default=0)

    # class Meta:
    #     unique_together = ('disease', 'symptom')


class WinterSymptDisease(models.Model):
    disease = models.ManyToManyField(Disease, related_name='winter_sympt_disease')
    symptom = models.ManyToManyField(Symptom, related_name='winter_sympt_disease')
    counter = models.IntegerField(default=0)

    # class Meta:
    #     unique_together = ('disease', 'symptom')


class SummerSymptDisease(models.Model):
    disease = models.ManyToManyField(Disease, related_name='summer_sympt_disease')
    symptom = models.ManyToManyField(Symptom, related_name='summer_sympt_disease')
    counter = models.IntegerField(default=0)

    # class Meta:
    #     unique_together = ('disease', 'symptom')


class AutumnSymptDisease(models.Model):
    disease = models.ManyToManyField(Disease, related_name='autumn_sympt_disease')
    symptom = models.ManyToManyField(Symptom, related_name='autumn_sympt_disease')
    counter = models.IntegerField(default=0)

    # class Meta:
    #     unique_together = ('disease', 'symptom')

class Specialization(models.Model):
    SPEC_CHOICES = (
        ('0', 'therapist'),
        ('1', 'neurologist'),
        ('2', 'ophthalmologist'),
        ('3', 'surgeon'),
        ('4', 'cardiologist'),
    )
    spec_type = models.CharField(max_length=2, choices=SPEC_CHOICES)
    def __str__(self):
        return self.spec_type

    class Meta:
        verbose_name = 'специальность'
        verbose_name_plural = 'специальности'

class Examination(models.Model):
    AGE_GROUP = (
        ('1', '< 1 года'),
        ('2', '1 - 5 лет'),
        ('3', '5 - 18 лет'),
        ('4', '18 - 60 лет'),
        ('5', '> 60 лет'),
    )
    doctor = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='врач')
    patient = models.CharField(max_length=50, verbose_name='ФИО пациента')
    age = models.CharField(max_length=1, blank=True, verbose_name='возраст', choices=AGE_GROUP)
    sex = models.CharField(max_length=1, choices= (('0', 'мужской'),('1', 'женский')), blank=True, verbose_name='пол')
    symptoms = models.ManyToManyField(to=Symptom, related_name="examinations", verbose_name='симптомы')
    contraindications = models.ManyToManyField(to=Contraindication, related_name="examinations", verbose_name='противопоказания')
    diseases = models.ManyToManyField(to=Disease, related_name="examinations", verbose_name='заболевания')
    meds = models.ManyToManyField(to=Med, related_name="examinations", verbose_name='лечащие препараты')
    date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.patient + str(self.date_time)

    class Meta:
        verbose_name = 'обследование'
        verbose_name_plural = 'обследования'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')
    bio = models.CharField(max_length=50, blank=True)
    organisation = models.CharField(max_length=50, blank=False, verbose_name='место работы')
    specialization = models.ManyToManyField(to=Specialization, related_name="specializations", verbose_name='специализации')
    is_chief = models.BooleanField(default=False, verbose_name='должность главного врача')

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'



class Notification(models.Model):
    CONFIRMED = 0
    REQUESTED = 1
    REJECTED = 2

    DIAGNOSIS_STATUS_CHOICES = (
        (CONFIRMED, 'Диагноз подтвержден'),
        (REQUESTED, 'Запрос на подтверждение диагноза'),
        (REJECTED, 'Диагноз отклонен'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    diagnosis = models.ForeignKey(Disease, on_delete=models.CASCADE, verbose_name='диагноз')
    description = models.CharField(max_length=255, blank=True, verbose_name='описание')
    status = models.IntegerField(blank=False, verbose_name='статус диагноза', choices=DIAGNOSIS_STATUS_CHOICES)
    date_time = models.DateTimeField(auto_now=True)
    is_readed = models.BooleanField(default=False, verbose_name='прочитано')

    def __str__(self):
        return self.diagnosis.name + ' ' + str(self.status)

    class Meta:
        verbose_name = "уведомление"
        verbose_name_plural = "уведомления"



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

