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

class Address(models.Model):
    postal_code = models.CharField(max_length=6, null=True, blank=True)
    unit_number = models.CharField(max_length=10, null=True, blank=True)
    address_line_1 = models.CharField(max_length=100, null=True, blank=True)
    address_line_2 = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.address_line_1}, {self.address_line_2}, {self.unit_number}, {self.postal_code}"


class People(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    nric = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, null=False)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, null=True)
    date_of_birth = models.DateField(null=False)
    marital_status = models.CharField(choices=MARITAL_STATUS_CHOICES, max_length=8, null=False)
    employment_status = models.CharField(choices=EMPLOYMENT_STATUS_CHOICES, max_length=10, null=False)
    retrenchment_date = models.DateField(null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    contact_info = models.CharField(max_length=8, null=True, blank=True, unique=False)
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
        return f"{self.name} ({self.nric})"


class Applicant(models.Model):
    applicant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    person = models.OneToOneField(People, on_delete=models.CASCADE, related_name='applicant_profile')

    def __str__(self):
        return f"Applicant {self.person.name} ({self.person.nric})"


class HouseholdMember(models.Model):
    householdmember_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='household_members')
    person = models.ForeignKey(People, on_delete=models.CASCADE, related_name='household_member_profile')
    relationship_to_applicant = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)

    def __str__(self):
        return f"{self.person.name} is a {self.relationship_to_applicant} of {self.applicant.person.name}"
