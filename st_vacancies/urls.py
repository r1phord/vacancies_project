from django.urls import path

from vacancies.views import MainView, CompanyView, AllVacanciesView, VacancyView, CategoryVacanciesView

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('vacancies/', AllVacanciesView.as_view(), name='vacancies'),
    path('vacancies/<int:vacancy_id>/', VacancyView.as_view(), name='vacancy'),
    path('vacancies/cat/<str:category>/', CategoryVacanciesView.as_view(), name='cat_vacancy'),
    path('companies/<int:company_id>/', CompanyView.as_view(), name='company')
]
