from django.contrib import admin

from vacancies.models import Vacancy, Company, Application, Specialty


class SpecialtyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Specialty, SpecialtyAdmin)


class VacancyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Vacancy, VacancyAdmin)


class CompanyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Company, CompanyAdmin)


class ApplicationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Application, ApplicationAdmin)
