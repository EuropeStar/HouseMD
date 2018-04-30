from django.contrib import admin

from core.models import *

# class Inline(admin.StackedInline):
#     model = AnalysisConstants
#     extra = 3
#
# class DiseaseAdmin(admin.ModelAdmin):
#     inlines = [ChoiceInline]


admin.site.register(Profile)
admin.site.register(Disease)
admin.site.register(Symptom)
admin.site.register(Med)
admin.site.register(Contraindication)
admin.site.register(Specialization)
admin.site.register(SideEffect)
admin.site.register(ActiveSubstance)
admin.site.register(Examination)
admin.site.register(Notification)
# Register your models here.
