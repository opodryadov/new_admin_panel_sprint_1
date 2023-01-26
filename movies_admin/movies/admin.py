from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,)

    list_display = (
        'title', 'type', 'file_path', 'creation_date', 'rating', 'created_at',
        'updated_at',
    )

    list_filter = ('type', 'creation_date', 'rating',)

    search_fields = ('title', 'description', 'id',)


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline,)

    list_display = ('full_name',)

    search_fields = ('full_name',)
