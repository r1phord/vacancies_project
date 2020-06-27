from random import randint

from vacancies import data
from vacancies.models import Company, Specialty, Vacancy


for company in data.companies:
    Company.objects.create(name=company['name'],
                           location=company['location'],
                           description='some description',
                           employee_count=randint(2, 1000))

for specialty in data.specialties:
    Specialty.objects.create(code=specialty['code'],
                             title=specialty['title'])

for job in data.jobs:
    Vacancy.objects.create(title=job['title'],
                           specialty=Specialty.objects.get(code=job['cat']),
                           company=Company.objects.get(name=job['company']),
                           skills=job['skills'],
                           description=job['desc'],
                           salary_min=job['salary_from'],
                           salary_max=job['salary_to'],
                           published_at=job['posted'])
