from django.contrib import admin
from .models import Scheme, EligibilityCriteria, Benefit

@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = ('scheme_id', 'scheme_name', 'description')
    search_fields = ('scheme_name',)

@admin.register(EligibilityCriteria)
class EligibilityCriteriaAdmin(admin.ModelAdmin):
    list_display = ('eligibility_criterion_id', 'scheme', 'criterion_type', 'criterion_value')
    search_fields = ('criterion_type', 'criterion_value')
    list_filter = ('scheme',)

@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin):
    list_display = ('benefit_id', 'scheme', 'benefit_type', 'description')
    search_fields = ('benefit_type',)
    list_filter = ('scheme',)
