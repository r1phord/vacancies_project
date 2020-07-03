from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from vacancies.views import MainView, CompanyView, VacanciesView, VacancyView, SpecialtyVacanciesView, \
    custom_handler500, custom_handler404

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('admin/', admin.site.urls),
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/<int:vacancy_id>/', VacancyView.as_view(), name='vacancy'),
    path('vacancies/cat/<str:specialty_code>/', SpecialtyVacanciesView.as_view(), name='cat_vacancy'),
    path('companies/<int:company_id>/', CompanyView.as_view(), name='company')
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
