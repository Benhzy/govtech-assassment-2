from django.urls import path
from .views import ApplicationListCreateView, ApplicationListApplicantView, ApplicationUpdateView

urlpatterns = [
    path('', ApplicationListCreateView.as_view(), name='application-list-create'),
    path('<uuid:pk>/', ApplicationUpdateView.as_view(), name='application-update'),
    path('applicant/<uuid:applicant_id>/', ApplicationListApplicantView.as_view(), name='applications-by-applicant'),
]
