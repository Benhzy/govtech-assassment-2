from django.urls import path
from .views import (
    SchemeListCreateView, SchemeDetailView,
    EligibilityCriteriaListCreateView, EligibilityCriteriaDetailView,
    BenefitListCreateView, BenefitDetailView
)

urlpatterns = [
    path('', SchemeListCreateView.as_view(), name='scheme-list-create'),
    path('<int:pk>/', SchemeDetailView.as_view(), name='scheme-detail'),

    path('eligibility/', EligibilityCriteriaListCreateView.as_view(), name='eligibility-criteria-list-create'),
    path('eligibility/<int:pk>/', EligibilityCriteriaDetailView.as_view(), name='eligibility-criteria-detail'),

    path('benefits/', BenefitListCreateView.as_view(), name='benefit-list-create'),
    path('benefits/<int:pk>/', BenefitDetailView.as_view(), name='benefit-detail'),
]
