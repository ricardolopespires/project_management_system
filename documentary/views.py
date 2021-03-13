from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Avg
from .models import Documentary, D_Review, D_Likes, Genre, D_Rating
from actor.models import Actor
from django.contrib.auth.models import User
from movie.forms import RateForm
import requests




def documentary_manager(request):
	documentary = Documentary.objects.all()

	paginator = Paginator(documentary, 9) # 3 posts in each page
	page = request.GET.get('page')
	try:
		paginas = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer deliver the first page
		paginas = paginator.page(1)
	except EmptyPage:
		# If page is out of range deliver last page of results
		paginas = paginator.page(paginator.num_pages)


	return render(request, 'documentary/index.html',{'documentary':documentary, 'page':page,'paginas':paginas} )



# Create your views here.
def documentary_search(request):
	query = request.GET.get('search')

	if query:
		url = 'http://www.omdbapi.com/?apikey=2d2a4142&s=' + query
		response = requests.get(url)
		documentary = response.json()
		

		return render(request, 'documentary/search.html',{'query': query,'documentary': documentary})

	return render(request, 'documentary/search.html')



def documentary_details(request, imdb_id):

	if Documentary.objects.filter(imdbID=imdb_id).exists():
		documentary = Documentary.objects.get(imdbID=imdb_id)
		reviews = D_Review.objects.filter(documentary=documentary)
		reviews_avg = reviews.aggregate(Avg('rate'))
		reviews_count = reviews.count()
		our_db = True

		context = {
			'documentary': documentary,
			'reviews': reviews,
			'reviews_avg': reviews_avg,
			'reviews_count': reviews_count,
			'our_db': our_db,
		}

	else:
		url = 'http://www.omdbapi.com/?apikey=2d2a4142&i=' + imdb_id
		response = requests.get(url)
		documentary = response.json()

		#Inject to our database bellow:

		rating_objs = []
		genre_objs = []
		actor_objs = []

		#For the actors
		actor_list = [x.strip() for x in documentary['Actors'].split(',')]

		for actor in actor_list:
			a, created = Actor.objects.get_or_create(name=actor)
			actor_objs.append(a)

		#For the Genre or categories
		genre_list = list(documentary['Genre'].replace(" ", "").split(','))

		for genre in genre_list:
			genre_slug = slugify(genre)
			g, created = Genre.objects.get_or_create(title=genre, slug=genre_slug)
			genre_objs.append(g)

		#For the Rate
		for rate in documentary['Ratings']:
			r, created = D_Rating.objects.get_or_create(source=rate['Source'], rating=rate['Value'])
			rating_objs.append(r)

		if documentary['Type'] == 'movie':
			m, created = Documentary.objects.get_or_create(
				Title=documentary['Title'],
				Year=documentary['Year'],
				Publish = '2001-01-01 00:00:00', 
				Created = '2001-01-01 00:00:00', 
    			Updated = '2001-01-01 00:00:00', 		
				Status =  'geral', 
				Popularity = 0,
				Rated=documentary['Rated'],
				Released=documentary['Released'],
				Runtime=documentary['Runtime'],
				Director=documentary['Director'],
				Writer=documentary['Writer'],
				Plot=documentary['Plot'],
				Language=documentary['Language'],
				Country=documentary['Country'],
				Awards=documentary['Awards'],
				Poster_url=documentary['Poster'],
				Metascore=documentary['Metascore'],				
				imdbRating=documentary['imdbRating'],
				imdbCount = '0', 
				imdbVotes=documentary['imdbVotes'],
				imdbID=documentary['imdbID'],
				Filmes_views = 0,
				Video = 0,
				Trailer = '',
				Watched  = 0,
				Type = documentary['Type'],
				DVD = " ",
				BoxOffice = " ",
				Production= " ",
				Website = " ",
                totalSeasons =  0,
				totalEpisodes =  " ",
				)
			m.Genre.set(genre_objs)
			m.Actors.set(actor_objs)
			m.Rating.set(rating_objs)

		else:
			m, created = Documentary.objects.get_or_create(
				Title=documentary['Title'],
				Year=documentary['Year'],
				Publish = '2001-01-01 00:00:00', 
				Created = '2001-01-01 00:00:00', 
    			Updated = '2001-01-01 00:00:00', 		
				Status =  'geral', 
				Popularity = 0,
				Rated=documentary['Rated'],
				Released=documentary['Released'],
				Runtime=documentary['Runtime'],
				Director=documentary['Director'],
				Writer=documentary['Writer'],
				Plot=documentary['Plot'],
				Language=documentary['Language'],
				Country=documentary['Country'],
				Awards=documentary['Awards'],
				Poster_url=documentary['Poster'],
				Metascore=documentary['Metascore'],				
				imdbRating=documentary['imdbRating'],
				imdbCount = '0', 
				imdbVotes=documentary['imdbVotes'],
				imdbID=documentary['imdbID'],
				Filmes_views = 0,
				Video = 0,
				Trailer = '',
				Watched  = 0,
				Type = documentary['Type'],
				DVD = " ",
				BoxOffice = " ",
				Production= " ",
				Website = " ",
                totalSeasons =  0,
				totalEpisodes =  " ",
				)

			m.Genre.set(genre_objs)
			m.Actors.set(actor_objs)
			m.D_Ratings.set(rating_objs)


		for actor in actor_objs:
			actor.documentarys.add(m)
			actor.save()

		m.save()
		our_db = False

		context = {
			'movie_data': movie_data,
			'our_db': our_db,
		}

	template = loader.get_template('documentary/details.html')

	return HttpResponse(template.render(context, request))


def genres(request, genre_slug):
	genre = get_object_or_404(Genre, slug=genre_slug)
	movies = Documentary.objects.filter(Genre=genre)

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
	movie = Documentary.objects.get(imdbID=imdb_id)
	user = request.user
	profile = Profile.objects.get(user=user)

	profile.to_watch.add(movie)

	return HttpResponseRedirect(reverse('movie-details', args=[imdb_id]))

def addMoviesWatched(request, imdb_id):
	movie = Documentary.objects.get(imdbID=imdb_id)
	user = request.user
	profile = Profile.objects.get(user=user)

	if profile.to_watch.filter(imdbID=imdb_id).exists():
		profile.to_watch.remove(movie)
		profile.watched.add(movie)
		
	else:
		profile.watched.add(movie)

	return HttpResponseRedirect(reverse('movie-details', args=[imdb_id]))


def Rate(request, imdb_id):
	movie = Documentary.objects.get(imdbID=imdb_id)
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

