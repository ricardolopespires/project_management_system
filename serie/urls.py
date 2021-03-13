from django.urls import path
from . import views


app_name = 'serie'



urlpatterns = [
    
    path('manager/', views.serie_templateview, name='manager'),
	path('search/', views.serie_search, name='search'),	
	path('<imdb_id>/details/', views.movieDetails, name='serie-details'),
]