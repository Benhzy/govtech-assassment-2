from rest_framework import serializers
from .models import Scheme, EligibilityCriteria, Benefit

class EligibilityCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EligibilityCriteria
        fields = ['eligibility_criterion_id', 'criterion_type', 'criterion_value', 'additional_conditions']
        read_only_fields = ['eligibility_criterion_id']

class BenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefit
        fields = ['benefit_id', 'benefit_type', 'description']
        read_only_fields = ['benefit_id']

class SchemeSerializer(serializers.ModelSerializer):
    eligibility_criteria = EligibilityCriteriaSerializer(many=True)
    benefits = BenefitSerializer(many=True)

    class Meta:
        model = Scheme
        fields = ['scheme_id', 'scheme_name', 'description', 'eligibility_criteria', 'benefits']
        read_only_fields = ['scheme_id']

    def create(self, validated_data):
        eligibility_criteria_data = validated_data.pop('eligibility_criteria', [])
        benefits_data = validated_data.pop('benefits', [])

        scheme = Scheme.objects.create(**validated_data)

        for criterion_data in eligibility_criteria_data:
            EligibilityCriteria.objects.create(scheme=scheme, **criterion_data)

        for benefit_data in benefits_data:
            Benefit.objects.create(scheme=scheme, **benefit_data)

        return scheme

    def update(self, instance, validated_data):
        eligibility_criteria_data = validated_data.pop('eligibility_criteria', [])
        benefits_data = validated_data.pop('benefits', [])

        instance.scheme_name = validated_data.get('scheme_name', instance.scheme_name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        instance.eligibility_criteria.all().delete()
        for criterion_data in eligibility_criteria_data:
            EligibilityCriteria.objects.create(scheme=instance, **criterion_data)

        instance.benefits.all().delete()
        for benefit_data in benefits_data:
            Benefit.objects.create(scheme=instance, **benefit_data)

        return instance

    def validate_eligibility_criteria(self, value):
        if not value:
            raise serializers.ValidationError("At least one eligibility criterion is required.")
        return value

    def validate_benefits(self, value):
        if not value:
            raise serializers.ValidationError("At least one benefit is required.")
        return value