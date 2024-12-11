from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Application, ApplicationScheme, ApplicationEligibility, ApplicationBenefit
from .serializers import ApplicationSerializer
from schemes.models import Scheme, EligibilityCriteria, Benefit
from applicants.models import Applicant

class ApplicationListCreateView(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        data = request.data
        applicant_id = data.get('applicant_id')
        schemes = data.get('schemes', [])

        try:
            applicant = Applicant.objects.get(applicant_id=applicant_id)
        except Applicant.DoesNotExist:
            return Response(
                {"error": "Invalid applicant ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not schemes:
            return Response(
                {"error": "At least one scheme must be provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        valid_schemes = Scheme.objects.filter(scheme_id__in=schemes)
        if valid_schemes.count() != len(schemes):
            return Response(
                {"error": "One or more provided scheme IDs are invalid."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            with transaction.atomic():
                application = Application.objects.create(
                    applicant=applicant,
                    application_status=data.get('application_status', 'Pending'),
                    remarks=data.get('remarks', ''),
                )

                for scheme in valid_schemes:
                    ApplicationScheme.objects.create(application=application, scheme=scheme)

                    for criterion in scheme.eligibility_criteria.all():
                        ApplicationEligibility.objects.create(
                            application=application,
                            eligibility_criterion=criterion,
                            is_met=self.meets_criterion(applicant, criterion)
                        )

                    for benefit in scheme.benefits.all():
                        ApplicationBenefit.objects.create(
                            application=application,
                            benefit=benefit,
                            awarded=False,  # Default logic, can be updated later
                            notes=""
                        )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            self.get_serializer(application).data,
            status=status.HTTP_201_CREATED
        )

    def meets_criterion(self, applicant, criterion):
        ctype = criterion.criterion_type
        cvalue = criterion.criterion_value
        person = applicant.person

        if ctype == 'age':
            operator = cvalue[0]
            threshold = int(cvalue[1:])
            if operator == '>':
                return person.age > threshold
            elif operator == '<':
                return person.age < threshold
            return False

        elif ctype == 'marital_status':
            return person.marital_status == cvalue

        elif ctype == 'sex':
            return person.sex == cvalue

        elif ctype == 'employment_status':
            return person.employment_status == cvalue

        elif ctype == 'current_education':
            return person.current_education == cvalue

        elif ctype == 'monthly_income':
            operator = cvalue[0]
            threshold = float(cvalue[1:])
            applicant_income = person.monthly_income if person.monthly_income is not None else 0.0
            if operator == '>':
                return applicant_income > threshold
            elif operator == '<':
                return applicant_income < threshold
            return False

        elif ctype == 'completed_national_service':
            required = (cvalue.lower() == 'true')
            return person.completed_national_service == required

        elif ctype == 'disability':
            required = (cvalue.lower() == 'true')
            return person.disability == required

        elif ctype == 'household_member_relationship':
            for member in applicant.household_members.all():
                if member.relationship_to_applicant == 'Child':
                    return True
            return False

        elif ctype == 'household_member_age':
            operator = cvalue[0]
            threshold = int(cvalue[1:])
            for member in applicant.household_members.all():
                if member.relationship_to_applicant == 'Child':
                    if operator == '>':
                        return person.age > threshold
                    elif operator == '<':
                        return person.age < threshold
            return False

        elif ctype == 'household_member_education':
            for member in applicant.household_members.all():
                if member.relationship_to_applicant == 'Child' and member.person.current_education == cvalue:
                    return True
            return False

        else:
            raise ValueError(f"Unknown criterion type: '{ctype}' is not in the system.")


class ApplicationDetailView(generics.RetrieveAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]