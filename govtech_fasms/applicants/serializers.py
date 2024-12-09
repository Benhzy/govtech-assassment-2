from rest_framework import serializers
from .models import Applicant, Address, HouseholdRelationship

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['postal_code', 'unit_number', 'address_line_1', 'address_line_2']


class HouseholdRelationshipSerializer(serializers.ModelSerializer):
    related_person = serializers.PrimaryKeyRelatedField(queryset=Applicant.objects.all())
    relationship_type = serializers.CharField()

    class Meta:
        model = HouseholdRelationship
        fields = ['related_person', 'relationship_type']


class ApplicantSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)
    relationships = HouseholdRelationshipSerializer(many=True, source='relationships_as_applicant', required=False)
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = Applicant
        fields = [
            'id',
            'name',
            'sex',
            'date_of_birth',
            'age',
            'marital_status',
            'employment_status',
            'retrenchment_date',
            'address',
            'contact_info',
            'current_education',
            'monthly_income',
            'completed_national_service',
            'relationships'
        ]

    def create(self, validated_data):
        relationships_data = validated_data.pop('relationships_as_applicant', [])
        address_data = validated_data.pop('address', None)
        address = Address.objects.create(**address_data) if address_data else None
        applicant = Applicant.objects.create(address=address, **validated_data)
        for relationship_data in relationships_data:
            HouseholdRelationship.objects.create(
                applicant=applicant,
                **relationship_data
            )
        return applicant

    def update(self, instance, validated_data):
        relationships_data = validated_data.pop('relationships_as_applicant', [])
        address_data = validated_data.pop('address', None)
        if address_data:
            if instance.address:
                for key, value in address_data.items():
                    setattr(instance.address, key, value)
                instance.address.save()
            else:
                instance.address = Address.objects.create(**address_data)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        instance.relationships_as_applicant.all().delete()
        for relationship_data in relationships_data:
            HouseholdRelationship.objects.create(
                applicant=instance,
                **relationship_data
            )
        return instance

    def delete(self, instance):
        instance.relationships_as_applicant.all().delete()
        instance.delete()
        return {'message': 'Applicant and associated references deleted successfully.'}
