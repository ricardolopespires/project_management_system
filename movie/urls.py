from django.urls import path
from . import views 


app_name = 'movie'


urlpatterns = [
	path('manager/', views.movie_templateview, name='manager'),
	path('search/', views.index, name='search'),	
	path('<imdb_id>/details/', views.movieDetails, name='movie-details'),
	path('<imdb_id>/addtomoviewatch', views.addMoviesToWatch, name='add-movies-to-watch'),
	path('<imdb_id>/addmoviewatched', views.addMoviesWatched, name='add-movies-watched'),
	path('genre/<slug:genre_slug>', views.genres, name='genres'),
	path('<imdb_id>/rate', views.Rate, name='rate-movie'),
]