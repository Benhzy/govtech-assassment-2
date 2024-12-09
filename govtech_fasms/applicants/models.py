import uuid
from django.db import models
from django.utils import timezone

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

RELATIONSHIP_CHOICES = [
    ('Spouse', 'Spouse'),
    ('Parent', 'Parent'),
    ('Child', 'Child'),
    ('Grandparent', 'Grandparent'),
    ('Grandchild', 'Grandchild'),
    ('Sibling', 'Sibling'),
    ('Guardian', 'Guardian'),
    ('Ward', 'Ward'),
]

SEX_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]

EDUCATION_CHOICES = [
    ('pre-primary', 'pre-primary'),
    ('primary', 'primary'),
    ('secondary', 'secondary'),
    ('tertiary', 'tertiary'),
    ('not in education', 'not in education'),
]

class Address(models.Model):
    postal_code = models.CharField(max_length=6, null=True, blank=True)
    unit_number = models.CharField(max_length=10, null=True, blank=True)
    address_line_1 = models.CharField(max_length=100, null=True, blank=True)
    address_line_2 = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.address_line_1}, {self.address_line_2}, {self.unit_number}, {self.postal_code}"


class Applicant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, null=False)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, null=True)
    date_of_birth = models.DateField(null=False)
    marital_status = models.CharField(choices=MARITAL_STATUS_CHOICES, max_length=8, null=False)
    employment_status = models.CharField(choices=EMPLOYMENT_STATUS_CHOICES, max_length=10, null=False)
    retrenchment_date = models.DateField(null=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)
    contact_info = models.CharField(max_length=8, null=True, blank=True, unique=True)
    current_education = models.CharField(max_length=20, choices=EDUCATION_CHOICES, null=True, blank=True)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    completed_national_service = models.BooleanField(default=False)

    @property
    def age(self):
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def __str__(self):
        return self.name


class HouseholdRelationship(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name="relationships_as_applicant")
    related_person = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name="relationships_as_related")
    relationship_type = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)

    class Meta:
        unique_together = ('applicant', 'related_person', 'relationship_type')

    def __str__(self):
        return f"{self.applicant.name} is {self.relationship_type} of {self.related_person.name}"
