from django.urls import path
from . import views


app_name = 'management'




urlpatterns = [

    path('management/index/',views.ManagementTemplateView.as_view(),name = 'index'),
    path('management/filmes/',views.FilmesTemplateView.as_view(), name = 'filmes_manager'),
    path('management/search/', views.movie_management, name = 'search'),
    path('<imdb_id>/', views.movieDetails, name = 'movie-details'),
   
    
]