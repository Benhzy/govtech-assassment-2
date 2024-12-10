from rest_framework import serializers
from .models import Application, ApplicationEligibility, ApplicationBenefit, ApplicationScheme
from schemes.models import Scheme, EligibilityCriteria

class EligibilityCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EligibilityCriteria
        fields = ['criterion_type', 'criterion_value', 'additional_conditions']

class ApplicationEligibilitySerializer(serializers.ModelSerializer):
    criterion_type = serializers.CharField(source='eligibility_criterion.criterion_type', read_only=True)
    criterion_value = serializers.CharField(source='eligibility_criterion.criterion_value', read_only=True)
    additional_conditions = serializers.CharField(source='eligibility_criterion.additional_conditions', read_only=True)

    class Meta:
        model = ApplicationEligibility
        fields = ['criterion_type', 'criterion_value', 'additional_conditions', 'is_met']

class ApplicationBenefitSerializer(serializers.ModelSerializer):
    benefit_type = serializers.CharField(source='benefit.benefit_type', read_only=True)
    description = serializers.CharField(source='benefit.description', read_only=True)

    class Meta:
        model = ApplicationBenefit
        fields = [
            'application_benefit_id', 'benefit', 'benefit_type',
            'description', 'awarded', 'notes']

class SchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheme
        fields = ['scheme_id', 'scheme_name', 'description']

class ApplicationSchemeSerializer(serializers.ModelSerializer):
    scheme = SchemeSerializer(read_only=True)

    class Meta:
        model = ApplicationScheme
        fields = ['scheme', 'added_date']

class ApplicationSerializer(serializers.ModelSerializer):
    application_eligibility = ApplicationEligibilitySerializer(many=True, read_only=True)
    application_benefits = ApplicationBenefitSerializer(many=True, read_only=True)
    schemes = SchemeSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'applicant', 'application_date', 'application_status',
            'decision_date', 'remarks', 'schemes',
            'application_eligibility', 'application_benefits']