from django.contrib import admin
from .models import Serie
# Register your models here.
from import_export.admin import ImportExportModelAdmin
# Register your models here.



@admin.register(Serie)
class ActorAdmin(ImportExportModelAdmin):
    list_display  = ['Title']