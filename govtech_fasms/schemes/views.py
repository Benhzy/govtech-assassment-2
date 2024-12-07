from rest_framework import generics, permissions
from .models import Scheme, EligibilityCriteria, Benefit
from .serializers import SchemeSerializer, EligibilityCriteriaSerializer, BenefitSerializer

class SchemeListCreateView(generics.ListCreateAPIView):
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer
    permission_classes = [permissions.IsAuthenticated]

class SchemeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer
    permission_classes = [permissions.IsAuthenticated]

class EligibilityCriteriaListCreateView(generics.ListCreateAPIView):
    queryset = EligibilityCriteria.objects.all()
    serializer_class = EligibilityCriteriaSerializer
    permission_classes = [permissions.IsAuthenticated]

class EligibilityCriteriaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EligibilityCriteria.objects.all()
    serializer_class = EligibilityCriteriaSerializer
    permission_classes = [permissions.IsAuthenticated]

class BenefitListCreateView(generics.ListCreateAPIView):
    queryset = Benefit.objects.all()
    serializer_class = BenefitSerializer
    permission_classes = [permissions.IsAuthenticated]

class BenefitDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Benefit.objects.all()
    serializer_class = BenefitSerializer
    permission_classes = [permissions.IsAuthenticated]
