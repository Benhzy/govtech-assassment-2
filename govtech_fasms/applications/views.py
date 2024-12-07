from rest_framework import generics, permissions
from .models import Application, ApplicationEligibility, ApplicationBenefit
from .serializers import ApplicationSerializer, ApplicationEligibilitySerializer, ApplicationBenefitSerializer

class ApplicationListCreateView(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

class ApplicationEligibilityListCreateView(generics.ListCreateAPIView):
    queryset = ApplicationEligibility.objects.all()
    serializer_class = ApplicationEligibilitySerializer
    permission_classes = [permissions.IsAuthenticated]

class ApplicationEligibilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationEligibility.objects.all()
    serializer_class = ApplicationEligibilitySerializer
    permission_classes = [permissions.IsAuthenticated]

class ApplicationBenefitListCreateView(generics.ListCreateAPIView):
    queryset = ApplicationBenefit.objects.all()
    serializer_class = ApplicationBenefitSerializer
    permission_classes = [permissions.IsAuthenticated]

class ApplicationBenefitDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationBenefit.objects.all()
    serializer_class = ApplicationBenefitSerializer
    permission_classes = [permissions.IsAuthenticated]
