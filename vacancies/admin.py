from django.contrib import admin

from vacancies.models import Vacancy, Company, Application


class VacancyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Vacancy, VacancyAdmin)


class CompanyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Company, CompanyAdmin)


class ApplicationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Application, ApplicationAdmin)
