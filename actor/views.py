from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader
from django.http import HttpResponse

from actor.models import Actor
from movie.models import Movie

# Create your views here.


def actors(request):	
	actors = Actor.objects.all()
	movies = Movie.objects.filter(Actors=actors)


	paginator = Paginator(actors, 9) # 3 posts in each page
	page = request.GET.get('page')
	try:
		paginas = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer deliver the first page
		paginas = paginator.page(1)
	except EmptyPage:
		# If page is out of range deliver last page of results
		paginas = paginator.page(paginator.num_pages)
	

	
	return render(request, 'actor/index.html',{	'paginas': paginas,'actors': actors, 'movies':movies})



def details(request, slug):
	actor = get_object_or_404(Actor, slug = slug)
	return render(request, 'actor/details.html',{'actor':actor})