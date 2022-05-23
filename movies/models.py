from pyexpat import model
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

""" Actors and Directors """
class ActorsAndDirectors(models.Model):
    name = models.CharField("Name", max_length=100)
    age = models.PositiveSmallIntegerField("Age", default=0)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to="actors/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Actors and Directors"
        verbose_name_plural = "Actors and Directors"

""" Genres """
class Genres(models.Model):
    name = models.CharField("Name", max_length=100)
    description = models.TextField("Description")
    url = models.SlugField(max_length=160, unique = True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
    
""" Movies """    
class Movies(models.Model):
    title = models.CharField("Title", max_length=100)
    description = models.TextField("Description")
    poster = models.ImageField("Poster", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Year")
    directors = models.ManyToManyField(ActorsAndDirectors, related_name="film_director")
    actors = models.ManyToManyField(ActorsAndDirectors, related_name="film_actor")
    genres = models.ManyToManyField(Genres)
    trailer_url = models.CharField("TrailerUrl", max_length=240, default="")
    movie_url = models.CharField("MovieUrl", max_length=240, default="")
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_comment(self):
        return self.comments_set.filter()

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

"""Кадры из фильма"""
class MovieShots(models.Model):
    title = models.CharField("Title", max_length=100)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to="movie_shots/")
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Movie Shot"
        verbose_name_plural = "Movie Shots"

"""Звезда рейтинга"""
class RatingStars(models.Model):
    value = models.SmallIntegerField("Value", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Rating star"    
        verbose_name_plural = "Rating stars"
        ordering = ["-value"]


"""Рейтинг"""
class Ratings(models.Model):
    ip = models.CharField("IP address", max_length=15)
    star = models.ForeignKey(RatingStars, on_delete=models.CASCADE, verbose_name="star")
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, verbose_name="movie")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"

class Comments(models.Model):
    text = models.TextField('text', max_length=5000, default="")
    date = models.DateTimeField('date', auto_now_add=True)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text} - {self.user}"
    
    def get_comment(self):
        return self.comments_set.filter()

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"