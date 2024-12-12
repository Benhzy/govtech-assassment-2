from rest_framework import serializers
from collections import OrderedDict
from django.db import transaction
from .models import Applicant, Address, HouseholdMember, People


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['postal_code', 'unit_number', 'address_line_1', 'address_line_2']


class PeopleSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False, allow_null=True)

    class Meta:
        model = People
        fields = [
            'nric', 'name', 'sex', 'date_of_birth', 'marital_status',
            'employment_status', 'retrenchment_date', 'address',
            'contact_info', 'current_education', 'monthly_income',
            'completed_national_service'
        ]

class HouseholdMemberSerializer(serializers.ModelSerializer):
    person = PeopleSerializer()

    class Meta:
        model = HouseholdMember
        fields = ['householdmember_id', 'person', 'relationship_to_applicant']
        read_only_fields = ['householdmember_id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        person_data = representation.pop('person')
        representation.update(person_data)
        return representation


class ApplicantSerializer(serializers.ModelSerializer):
    person = PeopleSerializer()
    household_members = HouseholdMemberSerializer(many=True, required=False)

    class Meta:
        model = Applicant
        fields = ['applicant_id', 'person', 'household_members']
        read_only_fields = ['applicant_id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        person_data = representation.pop('person')
        household_members = representation.pop('household_members', [])
        applicant_id = representation.pop('applicant_id', None)
        
        ordered_data = OrderedDict()
        ordered_data['applicant_id'] = applicant_id
        ordered_data.update(person_data)
        ordered_data['household_members'] = household_members
        
        return ordered_data