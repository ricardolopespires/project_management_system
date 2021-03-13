from django.contrib import admin
from .models import Actor
from import_export.admin import ImportExportModelAdmin
# Register your models here.



@admin.register(Actor)
class ActorAdmin(ImportExportModelAdmin):
    list_display  = ['name']
    search_fields = ['name']