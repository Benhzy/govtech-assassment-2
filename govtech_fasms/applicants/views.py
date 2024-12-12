from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db import transaction, IntegrityError
from datetime import datetime
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.db.models import ProtectedError
from .models import Applicant, People, HouseholdMember, Address
from .serializers import ApplicantSerializer

class CustomValidationError(DRFValidationError):
    def __init__(self, detail, code=None):
        if isinstance(detail, str):
            detail = {'error': detail}
        super().__init__(detail, code)

class ApplicantViewSet(viewsets.ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create_person(self, person_data):
        try:
            if isinstance(person_data.get('date_of_birth'), str):
                person_data['date_of_birth'] = datetime.strptime(person_data['date_of_birth'], '%Y-%m-%d').date()

            address_data = person_data.pop('address', None)
            if address_data:
                try:
                    address, _ = Address.objects.get_or_create(**address_data)
                    person_data['address'] = address
                except ValidationError as e:
                    raise CustomValidationError(f"Invalid address data: {str(e)}")

            person, created = People.objects.get_or_create(
                nric=person_data['nric'],
                defaults=person_data
            )
            
            if not created:
                for key, value in person_data.items():
                    setattr(person, key, value)
                person.save()
            return person

        except IntegrityError as e:
            if 'person_id' in str(e):
                raise CustomValidationError("A person with this ID already exists.")
            raise CustomValidationError(f"Database integrity error: {str(e)}")
        except ValueError as e:
            raise CustomValidationError(f"Invalid data format: {str(e)}")
        except Exception as e:
            raise CustomValidationError(f"Error creating person: {str(e)}")

    def handle_household_members(self, applicant, household_members_data):
        try:
            # First, clear existing household members if updating
            HouseholdMember.objects.filter(applicant=applicant).delete()
            
            for hm_data in household_members_data:
                person_data = {key: hm_data[key] for key in hm_data if key != 'relationship_to_applicant'}
                relationship_to_applicant = hm_data.get('relationship_to_applicant')
                
                if not relationship_to_applicant:
                    raise CustomValidationError("Relationship to applicant is required for household members")

                person = self.create_person(person_data)
                
                HouseholdMember.objects.create(
                    applicant=applicant,
                    person=person,
                    relationship_to_applicant=relationship_to_applicant
                )
        except Exception as e:
            raise CustomValidationError(f"Error handling household members: {str(e)}")

    def create(self, request, *args, **kwargs):
        try:
            validated_data = request.data
            if not validated_data:
                raise CustomValidationError("No data provided")

            household_members_data = validated_data.pop('household_members', [])

            with transaction.atomic():
                person = self.create_person(validated_data)
                applicant = Applicant.objects.create(person=person)
                if household_members_data:
                    self.handle_household_members(applicant, household_members_data)

            serializer = self.get_serializer(applicant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except CustomValidationError as e:
            return Response({'error': str(e.detail)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': f'An unexpected error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            validated_data = request.data

            if isinstance(validated_data.get('date_of_birth'), str):
                validated_data['date_of_birth'] = datetime.strptime(
                    validated_data['date_of_birth'], '%Y-%m-%d'
                ).date()

            household_members_data = validated_data.pop('household_members', [])

            with transaction.atomic():
                person_data = validated_data
                address_data = person_data.pop('address', None)

                if address_data:
                    self.handle_address_update(instance, address_data)

                for key, value in person_data.items():
                    setattr(instance.person, key, value)
                instance.person.save()

                if household_members_data is not None:
                    self.handle_household_members(instance, household_members_data)

            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        except CustomValidationError as e:
            return Response({'error': str(e.detail)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': f'An unexpected error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def handle_address_update(self, instance, address_data):
        try:
            if instance.person.address:
                existing_address = Address.objects.filter(
                    postal_code=address_data['postal_code']
                ).first()
                
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
            
            instance.person.save()
        except Exception as e:
            raise CustomValidationError(f"Error updating address: {str(e)}")

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(
                {"message": "Applicant successfully deleted."},
                status=status.HTTP_204_NO_CONTENT
            )
        except ProtectedError:
            return Response(
                {"error": "Cannot delete applicant as they have related records."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
