from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Scheme, EligibilityCriteria, Benefit
from .serializers import SchemeSerializer
from applicants.models import Applicant

from govtech_fasms.utils.eligibility import meets_criterion

class SchemeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        schemes = Scheme.objects.all()
        serializer = SchemeSerializer(schemes, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        scheme = get_object_or_404(Scheme, pk=pk)
        serializer = SchemeSerializer(scheme)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        try:
            scheme_name = data.get('scheme_name')
            description = data.get('description')
            eligibility_criteria = data.get('eligibility_criteria', [])
            benefits = data.get('benefits', [])

            scheme = Scheme.objects.create(scheme_name=scheme_name, description=description)

            for criterion in eligibility_criteria:
                EligibilityCriteria.objects.create(
                    scheme=scheme,
                    criterion_type=criterion.get('criterion_type'),
                    criterion_value=criterion.get('criterion_value'),
                    additional_conditions=criterion.get('additional_conditions', ''),
                )

            for benefit in benefits:
                Benefit.objects.create(
                    scheme=scheme,
                    benefit_type=benefit.get('benefit_type'),
                    description=benefit.get('description', ''),
                )

            serializer = SchemeSerializer(scheme)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": f"An error occurred while creating the scheme: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk=None):
        scheme = get_object_or_404(Scheme, pk=pk)
        data = request.data
        try:
            scheme.scheme_name = data.get('scheme_name', scheme.scheme_name)
            scheme.description = data.get('description', scheme.description)
            scheme.save()

            if 'eligibility_criteria' in data:
                scheme.eligibility_criteria.all().delete()
                for criterion in data['eligibility_criteria']:
                    EligibilityCriteria.objects.create(
                        scheme=scheme,
                        criterion_type=criterion.get('criterion_type'),
                        criterion_value=criterion.get('criterion_value'),
                        additional_conditions=criterion.get('additional_conditions', ''),
                    )

            if 'benefits' in data:
                scheme.benefits.all().delete()
                for benefit in data['benefits']:
                    Benefit.objects.create(
                        scheme=scheme,
                        benefit_type=benefit.get('benefit_type'),
                        description=benefit.get('description', ''),
                    )

            serializer = SchemeSerializer(scheme)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": f"An error occurred while updating the scheme: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def partial_update(self, request, pk=None):
        scheme = get_object_or_404(Scheme, pk=pk)
        data = request.data
        try:
            if 'scheme_name' in data:
                scheme.scheme_name = data['scheme_name']
            if 'description' in data:
                scheme.description = data['description']
            scheme.save()

            if 'eligibility_criteria' in data:
                scheme.eligibility_criteria.all().delete()
                for criterion in data['eligibility_criteria']:
                    EligibilityCriteria.objects.create(
                        scheme=scheme,
                        criterion_type=criterion.get('criterion_type'),
                        criterion_value=criterion.get('criterion_value'),
                        additional_conditions=criterion.get('additional_conditions', ''),
                    )

            if 'benefits' in data:
                scheme.benefits.all().delete()
                for benefit in data['benefits']:
                    Benefit.objects.create(
                        scheme=scheme,
                        benefit_type=benefit.get('benefit_type'),
                        description=benefit.get('description', ''),
                    )

            serializer = SchemeSerializer(scheme)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": f"An error occurred while partially updating the scheme: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk=None):
        scheme = get_object_or_404(Scheme, pk=pk)
        try:
            scheme.delete()
            return Response({"message": "Scheme successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"error": f"An error occurred while deleting the scheme: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'], url_path='eligible')
    def eligible(self, request):
        applicant_id = request.query_params.get('applicant', None)
        if not applicant_id:
            return Response({"detail": "Applicant ID not provided."}, status=status.HTTP_400_BAD_REQUEST)

        applicant = get_object_or_404(Applicant, pk=applicant_id)
        eligible_schemes = []

        for scheme in Scheme.objects.all():
            if self.applicant_is_eligible(applicant, scheme):
                eligible_schemes.append(scheme)

        serializer = SchemeSerializer(eligible_schemes, many=True)
        return Response(serializer.data)

    def applicant_is_eligible(self, applicant, scheme):
        for criterion in scheme.eligibility_criteria.all():
            if not meets_criterion(applicant, criterion):
                return False
        return True
