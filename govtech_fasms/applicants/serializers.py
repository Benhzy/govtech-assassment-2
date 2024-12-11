from rest_framework import serializers
from django.db import transaction
from .models import Applicant, Address, HouseholdMember, People


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address_id', 'postal_code', 'unit_number', 'address_line_1', 'address_line_2']


class HouseholdMemberSerializer(serializers.Serializer):
    nric = serializers.CharField()
    name = serializers.CharField()
    sex = serializers.CharField()
    date_of_birth = serializers.DateField()
    marital_status = serializers.CharField()
    employment_status = serializers.CharField()
    retrenchment_date = serializers.DateField(required=False, allow_null=True)
    address = AddressSerializer(required=False)
    contact_info = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    current_education = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    monthly_income = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    completed_national_service = serializers.BooleanField(required=False)
    relationship_to_applicant = serializers.CharField()

    def create_person(self, validated_data):
        people_fields = {
            'nric', 'name', 'sex', 'date_of_birth', 'marital_status',
            'employment_status', 'retrenchment_date', 'address',
            'contact_info', 'current_education', 'monthly_income',
            'completed_national_service'
        }
        person_data = {key: value for key, value in validated_data.items() if key in people_fields}

        address_data = person_data.pop('address', None)
        if address_data:
            address, _ = Address.objects.get_or_create(**address_data)
            person_data['address'] = address

        person, created = People.objects.get_or_create(nric=person_data['nric'], defaults=person_data)
        if not created:
            for key, value in person_data.items():
                setattr(person, key, value)
            person.save()

        return person

    def create(self, applicant, validated_data):
        person = self.create_person(validated_data)
        relationship_to_applicant = validated_data['relationship_to_applicant']
        return HouseholdMember.objects.create(
            applicant=applicant,
            person=person,
            relationship_to_applicant=relationship_to_applicant
        )


class ApplicantSerializer(serializers.Serializer):
    nric = serializers.CharField()
    name = serializers.CharField()
    sex = serializers.CharField()
    date_of_birth = serializers.DateField()
    marital_status = serializers.CharField()
    employment_status = serializers.CharField()
    retrenchment_date = serializers.DateField(required=False, allow_null=True)
    address = AddressSerializer(required=False)
    contact_info = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    current_education = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    monthly_income = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    completed_national_service = serializers.BooleanField(required=False)
    household_members = HouseholdMemberSerializer(many=True, required=False)

    def create_person(self, validated_data):
        people_fields = {
            'nric', 'name', 'sex', 'date_of_birth', 'marital_status',
            'employment_status', 'retrenchment_date', 'address',
            'contact_info', 'current_education', 'monthly_income',
            'completed_national_service'
        }
        person_data = {key: value for key, value in validated_data.items() if key in people_fields}

        address_data = person_data.pop('address', None)
        if address_data:
            address, _ = Address.objects.get_or_create(**address_data)
            person_data['address'] = address

        person, created = People.objects.get_or_create(nric=person_data['nric'], defaults=person_data)
        if not created:
            for key, value in person_data.items():
                setattr(person, key, value)
            person.save()

        return person

    def create(self, validated_data):
        household_members_data = validated_data.pop('household_members', [])

        with transaction.atomic():
            try:
                person = self.create_person(validated_data)
                applicant = Applicant.objects.create(person=person)

                for hm_data in household_members_data:
                    hm_serializer = HouseholdMemberSerializer(data=hm_data)
                    hm_serializer.is_valid(raise_exception=True)
                    hm_serializer.create(applicant, hm_serializer.validated_data)

                return applicant
            except Exception as e:
                raise serializers.ValidationError(f"An error occurred: {str(e)}")

    def to_representation(self, instance):
        return {
            "applicant_id": str(instance.applicant_id),
            "nric": instance.person.nric,
            "name": instance.person.name,
            "sex": instance.person.sex,
            "date_of_birth": instance.person.date_of_birth,
            "age": instance.person.age,
            "marital_status": instance.person.marital_status,
            "employment_status": instance.person.employment_status,
            "retrenchment_date": instance.person.retrenchment_date,
            "address": AddressSerializer(instance.person.address).data if instance.person.address else None,
            "contact_info": instance.person.contact_info,
            "current_education": instance.person.current_education,
            "monthly_income": instance.person.monthly_income,
            "completed_national_service": instance.person.completed_national_service,
            "household_members": [
                {
                    "householdmember_id": str(hm.householdmember_id),
                    "relationship_to_applicant": hm.relationship_to_applicant,
                    "nric": hm.person.nric,
                    "name": hm.person.name,
                    "sex": hm.person.sex,
                    "date_of_birth": hm.person.date_of_birth,
                    "marital_status": hm.person.marital_status,
                    "employment_status": hm.person.employment_status,
                    "retrenchment_date": hm.person.retrenchment_date,
                    "address": AddressSerializer(hm.person.address).data if hm.person.address else None,
                    "contact_info": hm.person.contact_info,
                    "current_education": hm.person.current_education,
                    "monthly_income": hm.person.monthly_income,
                    "completed_national_service": hm.person.completed_national_service,
                }
                for hm in instance.household_members.all()
            ]
        }

    def update(self, instance, validated_data):
        household_members_data = validated_data.pop('household_members', [])

        person_data = validated_data
        address_data = person_data.pop('address', None)

        if address_data:
            if instance.person.address:
                for key, value in address_data.items():
                    setattr(instance.person.address, key, value)
                instance.person.address.save()
            else:
                instance.person.address = Address.objects.create(**address_data)
        
        for key, value in person_data.items():
            setattr(instance.person, key, value)
        instance.person.save()

        existing_hm_ids = {str(hm.householdmember_id) for hm in instance.household_members.all()}
        new_hm_ids = {hm_data.get('householdmember_id') for hm_data in household_members_data if hm_data.get('householdmember_id')}

        for hm in instance.household_members.all():
            if str(hm.householdmember_id) not in new_hm_ids:
                hm.delete()

        for hm_data in household_members_data:
            if 'householdmember_id' in hm_data and hm_data['householdmember_id'] in existing_hm_ids:
                hm_instance = instance.household_members.get(householdmember_id=hm_data['householdmember_id'])
                HouseholdMemberSerializer().update(hm_instance, hm_data)
            else:
                hm_serializer = HouseholdMemberSerializer(data=hm_data)
                hm_serializer.is_valid(raise_exception=True)
                hm_serializer.create(instance, hm_serializer.validated_data)

        instance.save()
        return instance