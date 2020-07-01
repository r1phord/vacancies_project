from django.conf import settings
from django.urls import path, include

from vacancies.views import MainView, CompanyView, VacanciesView, VacancyView, SpecialtyVacanciesView, \
    custom_handler500, custom_handler404


handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/<int:vacancy_id>/', VacancyView.as_view(), name='vacancy'),
    path('vacancies/cat/<str:specialty_code>/', SpecialtyVacanciesView.as_view(), name='cat_vacancy'),
    path('companies/<int:company_id>/', CompanyView.as_view(), name='company')
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
