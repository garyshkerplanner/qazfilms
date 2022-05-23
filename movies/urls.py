from urllib.parse import urlparse
from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view()),
    path("filter/", views.FilterMoviesView.as_view(), name="filter"), 
    path("add-rating/", views.AddStarRating.as_view(), name="add_rating"), 
    path("search/", views.Search.as_view(), name="search"), 
    path("movies", views.MoviesView.as_view()),
    path("aboutus", views.AboutUsView.as_view()), 
    path("<slug:slug>/", views.MovieDetailView.as_view(), name="movie_detail"),
    path("comment/<str:slug>/", views.LeaveComment.as_view(), name="leave_comment"), 
    path("actor/<str:slug>/", views.ActorView.as_view(), name="actor_detail"),
]