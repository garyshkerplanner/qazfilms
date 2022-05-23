from atexit import register
from django import template
from movies.models import Movies

register = template.Library()

@register.inclusion_tag('movies/tags/last_movies.html')
def get_last_movies(count=5):
    movies = Movies.objects.order_by("-id")[:count]
    return {"last_movies": movies}