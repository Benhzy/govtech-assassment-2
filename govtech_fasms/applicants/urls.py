from django.urls import path
from .views import (
    ApplicantListCreateView, ApplicantDetailView,
    HouseholdMemberListCreateView, HouseholdMemberDetailView
)

urlpatterns = [
    path('', ApplicantListCreateView.as_view(), name='applicant-list-create'),
    path('<int:pk>/', ApplicantDetailView.as_view(), name='applicant-detail'),
    path('household-members/', HouseholdMemberListCreateView.as_view(), name='household-member-list-create'),
    path('household-members/<int:pk>/', HouseholdMemberDetailView.as_view(), name='household-member-detail'),
]
