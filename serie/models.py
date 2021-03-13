from django.db import models
from actor.models import Actor
from django.utils.text import slugify
import requests
from io import BytesIO
from django.core import files
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField 
from multiselectfield import MultiSelectField
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Genre(models.Model):
	title = models.CharField(max_length=25)
	slug = models.SlugField(null=False, unique=True)

	def get_absolute_url(self):
		return reverse('genres', args=[self.slug])

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.title.replace(" ", "")
			self.slug = slugify(self.title)
		return super().save(*args, **kwargs)

class S_Rating(models.Model):
	source = models.CharField(max_length=50)
	rating = models.CharField(max_length=10)

	def __str__(self):
		return self.source

class Serie(models.Model):

	STATUS_CHOICES = (
                        ('cartaz','Cartaz'),
                        ('em breve','Em Breve'),
                        ('lançamento','Lançamento'),
                        ('geral', 'Geral'),
                        ('novo','Novo')
                      )
	Title = models.CharField(max_length=200)
	Year = models.CharField(max_length=25, blank=True)
	Publish = models.DateTimeField(default=timezone.now,  blank=True)
	Created = models.DateTimeField(auto_now_add=True,  blank=True) 
	Updated = models.DateTimeField(auto_now=True,  blank=True)
	Status = models.CharField(max_length = 140, choices = STATUS_CHOICES , default = 'geral',  blank=True)  
	Popularity = models.IntegerField()
	Rated = models.CharField(max_length=10, blank=True)
	Released = models.CharField(max_length=25, blank=True)
	Runtime = models.CharField(max_length=25, blank=True)
	Genre = models.ManyToManyField(Genre, blank=True)
	Director = models.CharField(max_length=100, blank=True)
	Writer = models.CharField(max_length=300, blank=True)
	Actors = models.ManyToManyField(Actor, blank=True)
	Plot = models.CharField(max_length=900, blank=True)
	Language = models.CharField(max_length=300, blank=True)
	Country = models.CharField(max_length=100, blank=True)
	Awards = models.CharField(max_length=250, blank=True)
	Poster = models.ImageField(upload_to='movies', blank=True)
	Poster_url = models.URLField(blank=True)
	Rating = models.ManyToManyField(S_Rating, blank=True)
	Metascore = models.CharField(max_length=5, blank=True)	
	imdbRating = models.CharField(max_length=5, blank=True)
	imdbCount = models.CharField(max_length=100, blank=True)
	imdbVotes = models.CharField(max_length=100, blank=True)
	imdbID = models.CharField(max_length=100, blank=True)	
	Filmes_views = models.IntegerField(default=0,  blank=True)
	Video = models.IntegerField(default=0,  blank=True)
	Trailer = models.CharField(max_length=100, blank=True)
	Watched = models.IntegerField( default=0,  blank=True)  
	Type = models.CharField(max_length=10, blank=True)
	DVD = models.CharField(max_length=25, blank=True)
	BoxOffice = models.CharField(max_length=25, blank=True)
	Production = models.CharField(max_length=100, blank=True)
	Website = models.CharField(max_length=150, blank=True)
	totalSeasons = models.CharField(max_length=3, blank=True)
	totalEpisodes =  models.CharField(max_length=3, blank=True)

	def __str__(self):
		return self.Title

	def save(self, *args, **kwargs):
		if self.Poster == '' and self.Poster_url !='':
			resp = requests.get(self.Poster_url)
			pb = BytesIO()
			pb.write(resp.content)
			pb.flush()
			file_name = self.Poster_url.split("/")[-1]
			self.Poster.save(file_name, files.File(pb), save=False)

		return super().save(*args, **kwargs)

	def __str__(self):
		return self.Title

	def save(self, *args, **kwargs):
		if self.Poster == '' and self.Poster_url !='':
			resp = requests.get(self.Poster_url)
			pb = BytesIO()
			pb.write(resp.content)
			pb.flush()
			file_name = self.Poster_url.split("/")[-1]
			self.Poster.save(file_name, files.File(pb), save=False)

		return super().save(*args, **kwargs)


RATE_CHOICES = [
   	(1, '1 - Lixo'),
    (2, '2 - Horrível'),
    (3, '3 - Terrível'),
    (4, '4 - Ruim'),
    (5, '5 - OK'),
    (6, '6 - Watchable'),
    (7, '7 - Bom'),
    (8, '8 - Muito bom'),
    (9, '9 - Perfeito'),
    (10, '10 - Obra-prima '), 

]


class S_Review(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='serie_user_review', on_delete=models.CASCADE)
	serie = models.ForeignKey(Serie, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	text = models.TextField(max_length=3000, blank=True)
	rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)
	likes = models.PositiveIntegerField(default=0)
	unlikes = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.user.username

class Likes(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE, related_name='serie_user_like')
	type_like = models.PositiveSmallIntegerField()
	review = models.ForeignKey(S_Review, on_delete=models.CASCADE, related_name='serie_review_like')