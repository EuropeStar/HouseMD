from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ActiveSubstance(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "aктивное вещество"
        verbose_name_plural = "активные вещества"


class SideEffect(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "побочный эффект"
        verbose_name_plural = "побочные эффекты"


class Med(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField
    category = models.CharField(max_length=100)
    efficiency_class = models.IntegerField
    activeSubstances = models.ManyToManyField(ActiveSubstance, related_name='meds')
    side_effects = models.ManyToManyField(SideEffect, related_name='meds')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "препарат"
        verbose_name_plural = "препараты"


class Symptom(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "симптом"
        verbose_name_plural = "симптомы"


class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField
    probability = models.DecimalField
    meds = models.ManyToManyField(Med, related_name='diseases')

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
    probability = models.DecimalField

    # class Meta:
    #     unique_together = ('disease', 'symptom')


class WinterSymptDisease(models.Model):
    disease = models.ManyToManyField(Disease, related_name='winter_sympt_disease')
    symptom = models.ManyToManyField(Symptom, related_name='winter_sympt_disease')
    probability = models.DecimalField

    # class Meta:
    #     unique_together = ('disease', 'symptom')


class SummerSymptDisease(models.Model):
    disease = models.ManyToManyField(Disease, related_name='summer_sympt_disease')
    symptom = models.ManyToManyField(Symptom, related_name='summer_sympt_disease')
    probability = models.DecimalField

    # class Meta:
    #     unique_together = ('disease', 'symptom')


class AutumnSymptDisease(models.Model):
    disease = models.ManyToManyField(Disease, related_name='autumn_sympt_disease')
    symptom = models.ManyToManyField(Symptom, related_name='autumn_sympt_disease')
    probability = models.DecimalField

    # class Meta:
    #     unique_together = ('disease', 'symptom')

class Specialization(models.Model):
    SPEC_CHOICES = (
        ('0', 'therapist'),
    )
    student_type = models.CharField(max_length=2, choices=SPEC_CHOICES)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50, blank=False)
    organisation = models.CharField(max_length=50, blank=False)
    specialization = models.ManyToManyField(to=Specialization, related_name="specializations")
    is_chief = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
