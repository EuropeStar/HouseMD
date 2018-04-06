from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class AnalysisConstants(models.Model):
    name = models.CharField(max_length=50, verbose_name="параметр анализа", unique=True)
    lower_bound = models.DecimalField(verbose_name="нижняя граница", max_digits=10, decimal_places=4)
    upper_bound = models.DecimalField(verbose_name="верхняя граница", max_digits=10, decimal_places=4)

    # counter = models.PositiveIntegerField(verbose_name="встречаемость", default=0)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "критическое значения анализа"
        verbose_name_plural = "критические значения анализов"


class AnalysisParams(models.Model):
    name = models.ForeignKey(to=AnalysisConstants, related_name="analyses_set", verbose_name="параметр анализа",
                             on_delete=models.CASCADE)
    value = models.DecimalField(verbose_name="значение", max_digits=10, decimal_places=4)
    deviation = models.DecimalField(verbose_name="отклонение", max_digits=2, decimal_places=2)
    result = models.BooleanField(default=False, verbose_name="результат")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "параметр анализа"
        verbose_name_plural = "параметры анализа"


#
class ActiveSubstance(models.Model):
    name = models.CharField(max_length=100, verbose_name="название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "aктивное вещество"
        verbose_name_plural = "активные вещества"


#
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
    #
    activeSubstances = models.ManyToManyField(ActiveSubstance, related_name='meds', verbose_name='активные вещества')
    side_effects = models.ManyToManyField(SideEffect, related_name='meds', verbose_name='побочные эффекты')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "препарат"
        verbose_name_plural = "препараты"


class Symptom(models.Model):
    name = models.CharField(max_length=255, verbose_name='название')

    # counter = models.PositiveIntegerField(verbose_name="встречаемость", default=0)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "симптом"
        verbose_name_plural = "симптомы"


class Disease(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(verbose_name='описание', blank=True)
    meds = models.ManyToManyField(to=Med, related_name='diseases', verbose_name='используемые препараты')
    symptoms = models.ManyToManyField(to=Symptom, related_name='diseases', verbose_name='симптомы')
    analysis = models.ManyToManyField(to=AnalysisParams, related_name="diseases", verbose_name="анализы", )

    # counter = models.PositiveIntegerField(verbose_name="встречаемость", default=0)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "заболевание"
        verbose_name_plural = "заболевания"


class DiseaseProbability(models.Model):
    disease = models.ForeignKey(to=Disease, verbose_name="заболевание", on_delete=models.CASCADE)
    prob = models.DecimalField(verbose_name="вероятность", max_digits=2, decimal_places=2, default=0)

    def __str__(self):
        return self.disease.name + " " + str(self.prob)

    class Meta:
        verbose_name = "вероятность заболевания"
        verbose_name_plural = "вероятности заболеваний"

class Contraindication(models.Model):
    name = models.ForeignKey(ActiveSubstance, related_name='contraindications', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "противопоказание"
        verbose_name_plural = "противопоказания"

class Specialization(models.Model):
    SPEC_CHOICES = (
        ('0', 'терапевт'),
        ('1', 'невролог'),
        ('2', 'офтальмолог'),
        ('3', 'хирург'),
        ('4', 'кардиолог'),
    )
    spec_type = models.CharField(max_length=2, choices=SPEC_CHOICES)

    def __str__(self):
        return self.spec_type

    class Meta:
        verbose_name = 'специальность'
        verbose_name_plural = 'специальности'

class Examination(models.Model):
    AGE_GROUP = (
        ('0', '0'),
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
    diseases = models.ManyToManyField(to=DiseaseProbability, related_name="examinations", verbose_name='заболевания')
    meds = models.ManyToManyField(to=Med, related_name="examinations", verbose_name='лечащие препараты')
    date_time = models.DateTimeField(auto_now=True)

    #
    analysis = models.ManyToManyField(to=AnalysisParams, verbose_name="анализы", related_name="examinations")

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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

