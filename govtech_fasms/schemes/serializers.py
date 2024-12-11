from rest_framework import serializers
from .models import Scheme, EligibilityCriteria, Benefit

class EligibilityCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EligibilityCriteria
        fields = ['eligibility_criterion_id', 'criterion_type', 'criterion_value', 'additional_conditions']

class BenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefit
        fields = ['benefit_id', 'benefit_type', 'description', 'conditions']

class SchemeSerializer(serializers.ModelSerializer):
    eligibility_criteria = EligibilityCriteriaSerializer(many=True, read_only=True)
    benefits = BenefitSerializer(many=True, read_only=True)

    class Meta:
        model = Scheme
        fields = ['scheme_id', 'scheme_name', 'description', 'eligibility_criteria', 'benefits']
