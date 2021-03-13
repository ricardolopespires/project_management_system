from django.urls import path
from . import views


app_name = 'actor'


urlpatterns = [
	path('persona/', views.actors, name='index'),
	path('persona/<slug>/details/',views.details, name = 'details'),
]