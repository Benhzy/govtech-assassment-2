from rest_framework import serializers
from .models import Application, ApplicationEligibility, ApplicationBenefit

class ApplicationEligibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationEligibility
        fields = ['application_eligibility_id', 'eligibility_criterion', 'is_met']

class ApplicationBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationBenefit
        fields = ['application_benefit_id', 'benefit', 'awarded', 'notes']

class ApplicationSerializer(serializers.ModelSerializer):
    application_eligibility = ApplicationEligibilitySerializer(many=True, read_only=True)
    application_benefits = ApplicationBenefitSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = [
            'application_id', 'applicant', 'scheme', 'application_date',
            'application_status', 'decision_date', 'remarks',
            'application_eligibility', 'application_benefits'
        ]
