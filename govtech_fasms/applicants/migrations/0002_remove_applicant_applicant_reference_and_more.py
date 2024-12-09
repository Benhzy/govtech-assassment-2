# Generated by Django 5.1.4 on 2024-12-09 07:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicant',
            name='applicant_reference',
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='relationship_to_applicant',
        ),
        migrations.CreateModel(
            name='HouseholdRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relationship_type', models.CharField(choices=[('Spouse', 'Spouse'), ('Parent', 'Parent'), ('Child', 'Child'), ('Grandparent', 'Grandparent'), ('Grandchild', 'Grandchild'), ('Sibling', 'Sibling'), ('Guardian', 'Guardian'), ('Ward', 'Ward')], max_length=20)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationships_as_applicant', to='applicants.applicant')),
                ('related_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationships_as_related', to='applicants.applicant')),
            ],
            options={
                'unique_together': {('applicant', 'related_person', 'relationship_type')},
            },
        ),
    ]
