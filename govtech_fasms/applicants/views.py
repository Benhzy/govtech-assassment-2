from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db import transaction
from datetime import datetime
from .models import Applicant, People, HouseholdMember, Address
from .serializers import ApplicantSerializer

class ApplicantViewSet(viewsets.ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [AllowAny]

    def create_person(self, person_data):
        if isinstance(person_data.get('date_of_birth'), str):
            person_data['date_of_birth'] = datetime.strptime(person_data['date_of_birth'], '%Y-%m-%d').date()

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

    def handle_household_members(self, applicant, household_members_data):
        for hm_data in household_members_data:
            person_data = {key: hm_data[key] for key in hm_data if key != 'relationship_to_applicant'}
            relationship_to_applicant = hm_data['relationship_to_applicant']

            person = self.create_person(person_data)

            HouseholdMember.objects.create(
                applicant=applicant,
                person=person,
                relationship_to_applicant=relationship_to_applicant
            )

    def create(self, request, *args, **kwargs):
        validated_data = request.data
        household_members_data = validated_data.pop('household_members', [])

        with transaction.atomic():
            person = self.create_person(validated_data)
            applicant = Applicant.objects.create(person=person)
            self.handle_household_members(applicant, household_members_data)

        serializer = self.get_serializer(applicant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
 
def update(self, request, *args, **kwargs):
    instance = self.get_object()
    validated_data = request.data

    if isinstance(validated_data.get('date_of_birth'), str):
        validated_data['date_of_birth'] = datetime.strptime(validated_data['date_of_birth'], '%Y-%m-%d').date()

    household_members_data = validated_data.pop('household_members', [])

    with transaction.atomic():
        person_data = validated_data
        address_data = person_data.pop('address', None)

        if address_data:
            if instance.person.address:
                existing_address = Address.objects.filter(postal_code=address_data['postal_code']).first()
                if existing_address and existing_address != instance.person.address:
                    for key, value in address_data.items():
                        setattr(existing_address, key, value)
                    existing_address.save()
                    instance.person.address = existing_address
                else:
                    for key, value in address_data.items():
                        setattr(instance.person.address, key, value)
                    instance.person.address.save()
            else:
                instance.person.address = Address.objects.create(**address_data)

        for key, value in person_data.items():
            setattr(instance.person, key, value)
        instance.person.save()

        self.handle_household_members(instance, household_members_data)

    serializer = self.get_serializer(instance)
    return Response(serializer.data)
