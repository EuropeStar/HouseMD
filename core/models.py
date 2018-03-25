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
    name = models.CharField(max_length=100, verbose_name="название")
    description = models.TextField(verbose_name="описание", blank=True)
    category = models.CharField(max_length=100, blank=True, verbose_name="класс принадлежности")
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
    )
    spec_type = models.CharField(max_length=2, choices=SPEC_CHOICES)

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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
