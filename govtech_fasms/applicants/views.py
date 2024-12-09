from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from .models import Applicant
from .serializers import ApplicantSerializer

class ApplicantViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):

    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [AllowAny]
