from django.contrib import admin
from . models import Documentary
from import_export.admin import ImportExportModelAdmin
# Register your models here.


@admin.register(Documentary)
class DocumentaryAdmin(ImportExportModelAdmin):
    list_display = ['Title']
    list_search = ['Title']
