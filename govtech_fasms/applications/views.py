from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Application, ApplicationScheme, ApplicationBenefit
from .serializers import ApplicationSerializer
from schemes.models import Scheme 
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
                    application_scheme = ApplicationScheme.objects.create(
                        application=application,
                        scheme=scheme,
                    )
                    application_scheme.evaluate_eligibility(applicant)
                    
                    for benefit in scheme.benefits.all():
                        ApplicationBenefit.objects.create(
                            application_scheme=application_scheme,
                            benefit=benefit,
                            awarded=False,
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
    
class ApplicationListApplicantView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        applicant_id = self.kwargs.get('applicant_id')
        if not applicant_id:
            raise ValidationError({"error": "Applicant ID is required."})
        return Application.objects.filter(applicant__applicant_id=applicant_id)
    
class ApplicationUpdateView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        allowed_fields = ['application_status', 'remarks', 'decision_date']
        for field in allowed_fields:
            if field in data:
                setattr(instance, field, data[field])

        instance.save()
        return Response(
            self.get_serializer(instance).data,
            status=status.HTTP_200_OK
        )
