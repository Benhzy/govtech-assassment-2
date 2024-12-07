from django.db import models

MARITAL_STATUS_CHOICES = [
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Widowed', 'Widowed'),
    ('Divorced', 'Divorced'),
]

EMPLOYMENT_STATUS_CHOICES = [
    ('Employed', 'Employed'),
    ('Unemployed', 'Unemployed'),
]

class Applicant(models.Model):
    applicant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    date_of_birth = models.DateField(null=False)
    marital_status = models.CharField(choices=MARITAL_STATUS_CHOICES, max_length=8, null=False)
    employment_status = models.CharField(choices=EMPLOYMENT_STATUS_CHOICES, max_length=10, null=False)
    retrenchment_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    contact_info = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

class HouseholdMember(models.Model):
    household_member_id = models.AutoField(primary_key=True)
    applicant = models.ForeignKey(Applicant, related_name='household_members', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    relationship_to_applicant = models.CharField(max_length=50, null=False)
    date_of_birth = models.DateField(null=False)
    is_school_going = models.BooleanField(null=False)

    def __str__(self):
        return f"{self.name} ({self.relationship_to_applicant})"
