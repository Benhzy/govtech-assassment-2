from django.db import models

class Scheme(models.Model):
    scheme_id = models.AutoField(primary_key=True)
    scheme_name = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.scheme_name

class EligibilityCriteria(models.Model):
    eligibility_criterion_id = models.AutoField(primary_key=True)
    scheme = models.ForeignKey(Scheme, related_name='eligibility_criteria', on_delete=models.CASCADE)
    criterion_type = models.CharField(max_length=50, null=False)
    criterion_value = models.CharField(max_length=50, null=True, blank=True)
    additional_conditions = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Criteria for {self.scheme}: {self.criterion_type}"

class Benefit(models.Model):
    benefit_id = models.AutoField(primary_key=True)
    scheme = models.ForeignKey(Scheme, related_name='benefits', on_delete=models.CASCADE)
    benefit_type = models.CharField(max_length=50, null=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.benefit_type} for {self.scheme}"
