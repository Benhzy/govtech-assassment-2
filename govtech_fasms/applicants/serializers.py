from rest_framework import serializers
from .models import Applicant, HouseholdMember

class HouseholdMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseholdMember
        fields = ['household_member_id', 'name', 'relationship_to_applicant', 'date_of_birth', 'is_school_going']

class ApplicantSerializer(serializers.ModelSerializer):
    household_members = HouseholdMemberSerializer(many=True, required=False)

    class Meta:
        model = Applicant
        fields = [
            'applicant_id', 'name', 'date_of_birth', 'marital_status', 'employment_status',
            'retrenchment_date', 'address', 'contact_info', 'household_members'
        ]

    def create(self, validated_data):
        household_data = validated_data.pop('household_members', [])
        applicant = Applicant.objects.create(**validated_data)
        for member_data in household_data:
            HouseholdMember.objects.create(applicant=applicant, **member_data)
        return applicant
