from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ['person']


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = ('title', 'type', 'creation_date', 'rating', 'get_genres',)
    list_filter = ('type', 'creation_date', 'rating',)
    search_fields = ('title', 'description', 'id',)
    list_prefetch_related = ('genres',)

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ','.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = _('movie genres')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline,)
    list_display = ('full_name',)
    search_fields = ('full_name',)
