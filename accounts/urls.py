from django.urls import path
from . import views



urlpatterns = [

    path('login/',views.loggin, name = 'login'),
    path('register/',views.register, name = 'register'),

    
]


