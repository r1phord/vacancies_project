from django.urls import path

from vacancies.views import MainView, CompanyView, AllVacanciesView, VacancyView, CategoryVacanciesView

urlpatterns = [
    path('', MainView.as_view()),
    path('vacancies/', AllVacanciesView.as_view()),
    path('vacancies/<int:vacancy_id>/', VacancyView.as_view()),
    path('vacancies/cat/<str:category>/', CategoryVacanciesView.as_view()),
    path('companies/<int:company_id>/', CompanyView.as_view())
]
