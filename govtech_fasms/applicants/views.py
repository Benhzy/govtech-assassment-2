from rest_framework import generics, permissions
from .models import Applicant, HouseholdMember
from .serializers import ApplicantSerializer, HouseholdMemberSerializer

class ApplicantListCreateView(generics.ListCreateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [permissions.IsAuthenticated]

class ApplicantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [permissions.IsAuthenticated]

class HouseholdMemberListCreateView(generics.ListCreateAPIView):
    queryset = HouseholdMember.objects.all()
    serializer_class = HouseholdMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

class HouseholdMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HouseholdMember.objects.all()
    serializer_class = HouseholdMemberSerializer
    permission_classes = [permissions.IsAuthenticated]
