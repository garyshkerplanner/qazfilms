from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from movies.forms import RatingForm, CommentForm
from movies.models import ActorsAndDirectors, Comments, Genres, Movies, Ratings
from django.contrib.auth.models import User

class GenreYear:
    def get_genres(self):
        return Genres.objects.all()

    def get_years(self):
        return Movies.objects.filter(draft=False).values("year").distinct().order_by("year")

class HomeView(View):
    def get(self, request):
        featured_movie = Movies.objects.latest('id')
        popular_movies = Movies.objects.all().order_by('-id')[:9]
        bundle1, bundle2, bundle3 = zip(*[iter(popular_movies)]*3)
        context = {
            'featured_movie': featured_movie,
            'bundle1': bundle1,
            'bundle2': bundle2,
            'bundle3': bundle3
        }
        return render(request, "movies/index.html", context)

class MoviesView(GenreYear, ListView):
    model = Movies
    queryset = Movies.objects.filter(draft=False)

class AboutUsView(View):
    def get(self, request):
        return render(request, "movies/aboutus.html")

class MovieDetailView(GenreYear, DetailView):
    model = Movies
    queryset = Movies.objects.filter(draft=False)
    slug_field = "url"
    template_name = "movies/movie_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        context['form'] = CommentForm()
        context['movie'] = Comments.objects.filter(movie=kwargs['object'].id)
        return context

    def get_user_stars(self, ip, movie_id):
        if Ratings.objects.filter(ip=ip, movie_id=movie_id).exists():
            stars = Ratings.objects.get(ip=ip, movie_id=movie_id).star
        else:
            stars = None
        return stars

    def get(self, request, *args, **kwargs):

        ip = AddStarRating.get_client_ip(self, self.request)

        movie_id = Movies.objects.get(url=kwargs['slug']).id
        stars = self.get_user_stars(ip, movie_id)
    
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if stars:
            context['stars'] = str(stars)
            
        return self.render_to_response(context)

class ActorView(GenreYear, DetailView):
    model = ActorsAndDirectors
    template_name = 'movies/actor.html'
    slug_field = "name"

class FilterMoviesView(GenreYear, ListView):
    def get_queryset(self):
        if Movies.objects.filter(Q(year__in=self.request.GET.getlist("year"))).exists() and Movies.objects.filter(Q(genres__in=self.request.GET.getlist("genre"))):
            queryset = Movies.objects.filter(Q(year__in=self.request.GET.getlist("year"))).filter(Q(genres__in=self.request.GET.getlist("genre")))
        else:
            if Movies.objects.filter(Q(year__in=self.request.GET.getlist("year"))).exists():
                queryset = Movies.objects.filter(Q(year__in=self.request.GET.getlist("year")))
            elif Movies.objects.filter(Q(genres__in=self.request.GET.getlist("genre"))):
                queryset = Movies.objects.filter(Q(genres__in=self.request.GET.getlist("genre")))
        return queryset

class AddStarRating(View):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Ratings.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

class Search(GenreYear, ListView):
    def get_queryset(self):
        return Movies.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context

class LeaveComment(View):
    def post(self, request, slug):
        new_comment = Comments(text=request.POST.get('text'),
                                user=User.objects.get(id=request.user.id),
                                movie=Movies.objects.get(url=slug))
        new_comment.save()
        return redirect("movie_detail", slug = slug)
