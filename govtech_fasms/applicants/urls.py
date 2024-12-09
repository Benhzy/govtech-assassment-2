from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApplicantViewSet

router = DefaultRouter()
router.register('', ApplicantViewSet, basename='applicant')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
