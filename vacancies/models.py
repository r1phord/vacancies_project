from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=50)
    logo = models.URLField(default='https://place-hold.it/100x60')
    description = models.CharField(max_length=350)
    employee_count = models.PositiveIntegerField()


class Specialty(models.Model):
    code = models.CharField(max_length=25)
    title = models.CharField(max_length=25)
    picture = models.URLField(default='https://place-hold.it/100x60')


class Vacancy(models.Model):
    title = models.CharField(max_length=75)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.CharField(max_length=350)
    description = models.CharField(max_length=700)
    salary_min = models.PositiveIntegerField()
    salary_max = models.PositiveIntegerField()
    published_at = models.DateField()
