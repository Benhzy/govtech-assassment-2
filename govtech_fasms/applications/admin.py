from django.contrib import admin
from .models import Application, ApplicationEligibility, ApplicationBenefit

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('application_id', 'applicant', 'scheme', 'application_date', 'application_status', 'decision_date')
    search_fields = ('applicant__name', 'scheme__scheme_name')
    list_filter = ('application_status', 'scheme')

@admin.register(ApplicationEligibility)
class ApplicationEligibilityAdmin(admin.ModelAdmin):
    list_display = ('application_eligibility_id', 'application', 'eligibility_criterion', 'is_met')
    list_filter = ('is_met',)

@admin.register(ApplicationBenefit)
class ApplicationBenefitAdmin(admin.ModelAdmin):
    list_display = ('application_benefit_id', 'application', 'benefit', 'awarded')
    list_filter = ('awarded',)
