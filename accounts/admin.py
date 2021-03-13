from django.contrib import admin
from .models import User

# Registre suas modelos aqui.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username']


