from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Avg
from .models import Serie, Genre, S_Rating, S_Review
from actor.models import Actor
from django.contrib.auth.models import User


from movie.forms import RateForm

import requests




def serie_templateview(request):
	serie_data = Serie.objects.all()
	
	return render(request, 'serie/index.html',{'serie_data':serie_data})
  




def serie_search(request):
	query = request.GET.get('search')

	if query is not None:
		url = 'http://www.omdbapi.com/?apikey=2d2a4142&s=' + query
		response = requests.get(url)
		serie_data = response.json()
		
		return render(request, 'serie/search.html',{ 'query': query, 'serie_data': serie_data, 'page_number': 1,	})

	return render(request, 'serie/search.html')




def movieDetails(request, imdb_id):

	if Serie.objects.filter(imdbID=imdb_id).exists():
		serie_data = Serie.objects.get(imdbID=imdb_id)
		reviews = S_Review.objects.filter(serie=serie_data)
		reviews_avg = reviews.aggregate(Avg('rate'))
		reviews_count = reviews.count()
		our_db = True

		context = {
			'serie_data': serie_data,
			'reviews': reviews,
			'reviews_avg': reviews_avg,
			'reviews_count': reviews_count,
			'our_db': our_db,
		}

	else:
		url = 'http://www.omdbapi.com/?apikey=2d2a4142&i=' + imdb_id
		response = requests.get(url)
		serie_data = response.json()

		#Inject to our database bellow:

		rating_objs = []
		genre_objs = []
		actor_objs = []

		#For the actors
		actor_list = [x.strip() for x in serie_data['Actors'].split(',')]

		for actor in actor_list:
			a, created = Actor.objects.get_or_create(name=actor)
			actor_objs.append(a)

		#For the Genre or categories
		genre_list = list(serie_data['Genre'].replace(" ", "").split(','))

		for genre in genre_list:
			genre_slug = slugify(genre)
			g, created = Genre.objects.get_or_create(title=genre, slug=genre_slug)
			genre_objs.append(g)

		#For the Rate
		for rate in serie_data['Ratings']:
			r, created = S_Rating.objects.get_or_create(source=rate['Source'], rating=rate['Value'])
			rating_objs.append(r)

		if serie_data['Type'] == 'series':
			m, created = Serie.objects.get_or_create(
				Title=serie_data['Title'],
				Year=serie_data['Year'],
				Publish = '2001-01-01 00:00:00', 
				Created = '2001-01-01 00:00:00', 
    			Updated = '2001-01-01 00:00:00', 		
				Status =  'geral', 
				Popularity = 0,
				Rated=serie_data['Rated'],
				Released=serie_data['Released'],
				Runtime=serie_data['Runtime'],
				Director=serie_data['Director'],
				Writer=serie_data['Writer'],
				Plot=serie_data['Plot'],
				Language=serie_data['Language'],
				Country=serie_data['Country'],
				Awards=serie_data['Awards'],
				Poster_url=serie_data['Poster'],
				Metascore=serie_data['Metascore'],				
				imdbRating=serie_data['imdbRating'],
				imdbCount = '0', 
				imdbVotes=serie_data['imdbVotes'],
				imdbID=serie_data['imdbID'],
				Filmes_views = 0,
				Video = 0,
				Trailer = '',
				Watched  = 0,
				Type=serie_data['Type'],
				DVD = " ",
				BoxOffice = " ",
				Production= " ",
				Website = " ",
                totalSeasons=serie_data['totalSeasons'],
				totalEpisodes = 0,				
				)
			m.Genre.set(genre_objs)
			m.Actors.set(actor_objs)
			m.Rating.set(rating_objs)

		else:
			m, created = Serie.objects.get_or_create(
			Title=serie_data['Title'],
				Year=serie_data['Year'],
				Publish = '2001-01-01 00:00:00', 
				Created = '2001-01-01 00:00:00', 
    			Updated = '2001-01-01 00:00:00', 		
				Status =  'geral', 
				Popularity = 0,
				Rated=serie_data['Rated'],
				Released=serie_data['Released'],
				Runtime=serie_data['Runtime'],
				Director=serie_data['Director'],
				Writer=serie_data['Writer'],
				Plot=serie_data['Plot'],
				Language=serie_data['Language'],
				Country=serie_data['Country'],
				Awards=serie_data['Awards'],
				Poster_url=serie_data['Poster'],
				Metascore=serie_data['Metascore'],				
				imdbRating=serie_data['imdbRating'],
				imdbCount = '0', 
				imdbVotes=serie_data['imdbVotes'],
				imdbID=serie_data['imdbID'],
				Filmes_views = 0,
				Video = 0,
				Trailer = '',
				Watched  = 0,
				Type=serie_data['Type'],
				DVD = " ",
				BoxOffice = " ",
				Production= " ",
				Website = " ",
                totalSeasons=serie_data['totalSeasons'],
				totalEpisodes = 0,
				)

			m.Genre.set(genre_objs)
			m.Actors.set(actor_objs)
			m.S_Ratings.set(rating_objs)


		for actor in actor_objs:
			actor.series.add(m)
			actor.save()

		m.save()
		our_db = False

		context = {
			'serie_data': serie_data,
			'our_db': our_db,
		}

	template = loader.get_template('serie/details.html')

	return HttpResponse(template.render(context, request))


def genres(request, genre_slug):
	genre = get_object_or_404(Genre, slug=genre_slug)
	movies = Movie.objects.filter(Genre=genre)

	#Pagination
	paginator = Paginator(movies, 9)
	page_number = request.GET.get('page')
	movie_data = paginator.get_page(page_number)

	context = {
		'movie_data': movie_data,
		'genre': genre,
	}


	template = loader.get_template('genre.html')

	return HttpResponse(template.render(context, request))


def addMoviesToWatch(request, imdb_id):
	movie = Movie.objects.get(imdbID=imdb_id)
	user = request.user
	profile = Profile.objects.get(user=user)

	profile.to_watch.add(movie)

	return HttpResponseRedirect(reverse('movie-details', args=[imdb_id]))

def addMoviesWatched(request, imdb_id):
	movie = Movie.objects.get(imdbID=imdb_id)
	user = request.user
	profile = Profile.objects.get(user=user)

	if profile.to_watch.filter(imdbID=imdb_id).exists():
		profile.to_watch.remove(movie)
		profile.watched.add(movie)
		
	else:
		profile.watched.add(movie)

	return HttpResponseRedirect(reverse('movie-details', args=[imdb_id]))


def Rate(request, imdb_id):
	movie = Movie.objects.get(imdbID=imdb_id)
	user = request.user

	if request.method == 'POST':
		form = RateForm(request.POST)
		if form.is_valid():
			rate = form.save(commit=False)
			rate.user = user
			rate.movie = movie
			rate.save()
			return HttpResponseRedirect(reverse('movie-details', args=[imdb_id]))
	else:
		form = RateForm()

	template = loader.get_template('rate.html')

	context = {
		'form': form, 
		'movie': movie,
	}

	return HttpResponse(template.render(context, request))





def serie_updated(request, imdb_id):
	serie = get_object_or_404(Serie, imdbID = imdb_id)
	form = SerieForm(request.POST or None, instance = serie)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse('serie:manager'))

	return render(request,'management/series/updated.html',{'form':form})



def serie_created(request):
	if request.method == 'POST':
		form = SerieForm(request.POST or None)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('serie:manager'))
	else:
		form = SerieForm()
	return render(request,'management/series/updated.html',{'form':form})




def serie_delete(request, imdb_id):
    serie = get_object_or_404(Serie, imdbID = imdb_id)    
    if request.method=='POST':
        serie.delete()        
        return HttpResponseRedirect(reverse('serie:manager'))
    return render(request, 'management/series/delete.html', {'serie':serie})

