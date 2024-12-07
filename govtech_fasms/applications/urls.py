from django.urls import path
from .views import (
    ApplicationListCreateView, ApplicationDetailView,
    ApplicationEligibilityListCreateView, ApplicationEligibilityDetailView,
    ApplicationBenefitListCreateView, ApplicationBenefitDetailView
)

urlpatterns = [
    path('', ApplicationListCreateView.as_view(), name='application-list-create'),
    path('<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),

    path('eligibility/', ApplicationEligibilityListCreateView.as_view(), name='application-eligibility-list-create'),
    path('eligibility/<int:pk>/', ApplicationEligibilityDetailView.as_view(), name='application-eligibility-detail'),

    path('benefits/', ApplicationBenefitListCreateView.as_view(), name='application-benefit-list-create'),
    path('benefits/<int:pk>/', ApplicationBenefitDetailView.as_view(), name='application-benefit-detail'),
]
