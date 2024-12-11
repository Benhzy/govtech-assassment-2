from django.db import models
import uuid
from applicants.models import Applicant
from schemes.models import Scheme, EligibilityCriteria, Benefit

APPLICATION_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
]

class Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    applicant = models.ForeignKey(Applicant, related_name='applications', on_delete=models.CASCADE)
    application_date = models.DateField(auto_now_add=True)
    application_status = models.CharField(
        choices=APPLICATION_STATUS_CHOICES, max_length=8, default='Pending'
    )
    decision_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    schemes = models.ManyToManyField(
        Scheme, related_name='applications', through='ApplicationScheme'
    )

    def str(self):
        return f"Application {self.id}: {self.applicant}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self._generate_unique_uuid()
        super(Application, self).save(*args, **kwargs)

    def _generate_unique_uuid(self):
        while True:
            new_uuid = uuid.uuid4()
            if not Application.objects.filter(id=new_uuid).exists():
                return new_uuid


class ApplicationScheme(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    added_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('application', 'scheme')

    def str(self):
        return f"Application {self.application.id} - Scheme {self.scheme.id}"


class ApplicationEligibility(models.Model):
    application_eligibility_id = models.AutoField(primary_key=True)
    application = models.ForeignKey(Application, related_name='application_eligibility', on_delete=models.CASCADE)
    eligibility_criterion = models.ForeignKey(EligibilityCriteria, on_delete=models.CASCADE)
    is_met = models.BooleanField(null=False)

    def __str__(self):
        return f"Application {self.application.id} - Criteria {self.eligibility_criterion.id}"


class ApplicationBenefit(models.Model):
    application_benefit_id = models.AutoField(primary_key=True)
    application = models.ForeignKey(Application, related_name='application_benefits', on_delete=models.CASCADE)
    benefit = models.ForeignKey(Benefit, on_delete=models.CASCADE)
    awarded = models.BooleanField(null=False)       # for tracking if the scheme benefit reached the applicant 
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Application {self.application.id} - Benefit {self.benefit.id}"
