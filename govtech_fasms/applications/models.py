from django.db import models
from applicants.models import Applicant
from schemes.models import Scheme, EligibilityCriteria, Benefit

APPLICATION_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
]

class Application(models.Model):
    application_id = models.AutoField(primary_key=True)
    applicant = models.ForeignKey(Applicant, related_name='applications', on_delete=models.CASCADE)
    scheme = models.ForeignKey(Scheme, related_name='applications', on_delete=models.CASCADE)
    application_date = models.DateField(auto_now_add=True)
    application_status = models.CharField(choices=APPLICATION_STATUS_CHOICES, max_length=8, default='Pending')
    decision_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Application {self.application_id}: {self.applicant} - {self.scheme}"

class ApplicationEligibility(models.Model):
    application_eligibility_id = models.AutoField(primary_key=True)
    application = models.ForeignKey(Application, related_name='application_eligibility', on_delete=models.CASCADE)
    eligibility_criterion = models.ForeignKey(EligibilityCriteria, on_delete=models.CASCADE)
    is_met = models.BooleanField(null=False)

    def __str__(self):
        return f"Application {self.application_id} - Criteria {self.eligibility_criterion_id}"

class ApplicationBenefit(models.Model):
    application_benefit_id = models.AutoField(primary_key=True)
    application = models.ForeignKey(Application, related_name='application_benefits', on_delete=models.CASCADE)
    benefit = models.ForeignKey(Benefit, on_delete=models.CASCADE)
    awarded = models.BooleanField(null=False)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Application {self.application_id} - Benefit {self.benefit_id}"
