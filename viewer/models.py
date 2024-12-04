from django.db import models

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'Product'

class Person(models.Model):
    SEX_CHOICES = [
        (1, 'Male'),
        (2, 'Female'),
    ]
    QUALIFICATION_CHOICES = [
        (1, 'High School'),
        (2, 'Associate Degree'),
        (3, "Bachelor's Degree"),
        (4, "Master's Degree"),
        (5, 'Doctorate'),
    ]
    YES_NO_CHOICES = [
        (1, 'Yes'),
        (2, 'No'),
    ]

    id = models.IntegerField(primary_key=True)
    age = models.IntegerField(null=True, blank=True)
    sex = models.IntegerField(choices=SEX_CHOICES, null=True, blank=True)
    qualification = models.IntegerField(choices=QUALIFICATION_CHOICES, null=True, blank=True)
    country = models.CharField(max_length=2, null=True, blank=True)
    death = models.IntegerField(choices=YES_NO_CHOICES, null=True, blank=True)
    disability = models.IntegerField(choices=YES_NO_CHOICES, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Person'

class Injection(models.Model):
    DRUG_CHOICES = [
        (1, 'Drug A'),
        (2, 'Drug B'),
    ]

    id = models.IntegerField(primary_key=True)
    drug = models.IntegerField(choices=DRUG_CHOICES, null=True, blank=True)
    injection = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Injection'
