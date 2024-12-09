from django.contrib import admin
from .models import Applicant, Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['postal_code', 'unit_number', 'address_line_1', 'address_line_2']
    search_fields = ['postal_code', 'address_line_1', 'address_line_2']

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'date_of_birth', 'marital_status', 'employment_status', 'contact_info']
    search_fields = ['name', 'contact_info']
    list_filter = ['marital_status', 'employment_status', 'sex', 'current_education', 'completed_national_service']
