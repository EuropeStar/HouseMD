from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class AnalysisConstants(models.Model):
    name = models.CharField(max_length=50, verbose_name="параметр анализа", unique=True)
    lower_bound = models.DecimalField(verbose_name="нижняя граница", default=0.0, max_digits=25, decimal_places=4)
    upper_bound = models.DecimalField(verbose_name="верхняя граница", max_digits=25, decimal_places=4)
    dimension = models.CharField(max_length=10, null=True, verbose_name="размерность")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "критическое значения анализа"
        verbose_name_plural = "критические значения анализов"


class AnalysisParams(models.Model):
    name = models.ForeignKey(to=AnalysisConstants, related_name="analyses_set", verbose_name="параметр анализа",
                             on_delete=models.CASCADE)
    value = models.DecimalField(verbose_name="значение", max_digits=25, decimal_places=4)
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
    name = models.CharField(max_length=100, verbose_name="название")
    description = models.TextField(verbose_name="описание", blank=True)
    category = models.CharField(max_length=100, blank=True, verbose_name="класс принадлежности")
    efficiency_class = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="класс эффективности")
    side_effects = models.ManyToManyField(SideEffect, related_name='meds', verbose_name='побочные эффекты')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "препарат"
        verbose_name_plural = "препараты"


class Symptom(models.Model):
    name = models.CharField(max_length=255, verbose_name='название')

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
    analysis_constants = models.ManyToManyField(to=AnalysisConstants, related_name="diseases", verbose_name="анализы",
                                                through="DiseaseAnalysis")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "заболевание"
        verbose_name_plural = "заболевания"


class DiseaseAnalysis(models.Model):
    disease = models.ForeignKey(to=Disease, verbose_name="заболевание", on_delete=models.CASCADE)
    analysis = models.ForeignKey(to=AnalysisConstants, verbose_name="анализ", on_delete=models.CASCADE)
    sign = models.CharField(max_length=2, verbose_name='знак отклонения',
                            choices=(('<', '<'), ('>', '>'), ('<>', '<>')), default='<>')


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
    THERAPIST = 0
    NEUROLOGIST = 1
    OPHTHALMOLOGIST = 2
    SURGEON = 3
    CARDIOLOGIST = 4
    SPEC_CHOICES = (
        (THERAPIST, 'терапевт'),
        (NEUROLOGIST, 'невролог'),
        (OPHTHALMOLOGIST, 'офтальмолог'),
        (SURGEON, 'хирург'),
        (CARDIOLOGIST, 'кардиолог'),
    )
    spec_type = models.CharField(max_length=2, choices=SPEC_CHOICES)

    def __str__(self):
        return self.spec_type

    class Meta:
        verbose_name = 'специальность'
        verbose_name_plural = 'специальности'


class Examination(models.Model):
    MALE = 0
    FEMALE = 1

    LESS_ZERO_AGE = 0
    ZERO_ONE_AGE = 1
    ONE_FIVE_AGE = 2
    FIVE_EIGHTEEN_AGE = 3
    EIGHTEEN_SIXTY_AGE = 4
    MORE_SIXTY_AGE = 5
    AGE_GROUP = (
        (LESS_ZERO_AGE, '0'),
        (ZERO_ONE_AGE, '< 1 года'),
        (ONE_FIVE_AGE, '1 - 5 лет'),
        (FIVE_EIGHTEEN_AGE, '5 - 18 лет'),
        (EIGHTEEN_SIXTY_AGE, '18 - 60 лет'),
        (MORE_SIXTY_AGE, '> 60 лет'),
    )
    doctor = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='врач')
    patient = models.CharField(max_length=50, verbose_name='ФИО пациента')
    age = models.CharField(max_length=1, blank=True, verbose_name='возраст', choices=AGE_GROUP)
    sex = models.CharField(max_length=1, choices=((MALE, 'мужской'), (FEMALE, 'женский')), blank=True,
                           verbose_name='пол')
    symptoms = models.ManyToManyField(to=Symptom, related_name="examinations", verbose_name='симптомы')
    contraindications = models.ManyToManyField(to=Contraindication, related_name="examinations",
                                               verbose_name='противопоказания')
    diseases = models.ManyToManyField(to=DiseaseProbability, related_name="examinations", verbose_name='заболевания')
    meds = models.ManyToManyField(to=Med, related_name="examinations", verbose_name='лечащие препараты')
    date_time = models.DateTimeField(auto_now=True)
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
    specialization = models.ManyToManyField(to=Specialization, related_name="specializations",
                                            verbose_name='специализации')
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
