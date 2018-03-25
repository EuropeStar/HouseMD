from django.db import models


class ActiveSubstance(models.Model):
    name = models.CharField(max_length=100)


class SideEffect(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField


class Med(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField
    category = models.CharField(max_length=100)
    efficiency_class = models.IntegerField
    activeSubstances = models.ManyToManyField(ActiveSubstance, related_name='meds')
    side_effects = models.ManyToManyField(SideEffect, related_name='meds')


class Symptom(models.Model):
    name = models.CharField(max_length=100)


class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField
    probability = models.DecimalField
    meds = models.ManyToManyField(Med, related_name='diseases')


class Contraindication(models.Model):
    name = models.ForeignKey(ActiveSubstance, related_name='contraindications', on_delete=models.CASCADE)


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