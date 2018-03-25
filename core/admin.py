from django.contrib import admin

from core.models import *

admin.site.register(Profile)
admin.site.register(Disease)
admin.site.register(Symptom)
admin.site.register(Med)
# admin.site.register(Contraindication)
# admin.site.register(Specialization)
admin.site.register(SideEffect)
admin.site.register(ActiveSubstance)
# Register your models here.
