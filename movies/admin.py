from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import ActorsAndDirectors, Genres, Movies, RatingStars, Ratings, MovieShots, Comments

@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ("title", "year")
    list_filter = ("year", "genres")
    search_fields = ("title", )
    actions = ["publish", "unpublish"]

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 field was updated"
        else:
            message_bit = f"{row_update} fields were updated"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 field was updated"
        else:
            message_bit = f"{row_update} fields were updated"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Publish"
    publish.allowed_permissions = ('change', )

    unpublish.short_description = "Archive"
    unpublish.allowed_permissions = ('change',)

@admin.register(ActorsAndDirectors)
class ActorsAndDirectorsAdmin(admin.ModelAdmin):
    list_display = ("name", "get_image")
    search_fields = ("name", )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" height="100"')

@admin.register(Genres)
class Genres(admin.ModelAdmin):
    search_fields = ("name", )
    
@admin.register(Ratings)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("star", "movie", "ip")

@admin.register(MovieShots)
class MovieShots(admin.ModelAdmin):
    list_display = ("description", "get_image")
    search_fields = ("name", )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="160" height="100"')

admin.site.register(RatingStars)
admin.site.register(Comments)
