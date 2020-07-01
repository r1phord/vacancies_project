from django.contrib.auth.models import User
from django.db import models

from st_vacancies.settings import MEDIA_COMPANY_IMAGE_DIR


class Company(models.Model):
    name = models.CharField(max_length=120)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    location = models.CharField(max_length=50)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR)
    description = models.CharField(max_length=350)
    employee_count = models.PositiveIntegerField()


class Specialty(models.Model):
    code = models.CharField(max_length=25)
    title = models.CharField(max_length=25)
    picture = models.ImageField(upload_to='MEDIA_SPECIALITY_IMAGE_DIR')


class Vacancy(models.Model):
    title = models.CharField(max_length=75)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.CharField(max_length=350)
    description = models.CharField(max_length=700)
    salary_min = models.PositiveIntegerField()
    salary_max = models.PositiveIntegerField()
    published_at = models.DateField()


class Application(models.Model):
    written_username = models.CharField(max_length=20)
    written_phone = models.CharField(max_length=20)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')

