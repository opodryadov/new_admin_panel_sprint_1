import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(_('created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated'), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class FilmType(models.TextChoices):
    MOVIE = 'movie', _('movie')
    TV_SHOW = 'tv_show', _('tv_show')


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), null=True, blank=True)
    creation_date = models.DateField(_('creation date'), null=True, blank=True)
    file_path = models.FileField(_('file'), blank=True, null=True,
                                 upload_to='movies/')
    rating = models.FloatField(_('rating'), null=True, blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(10)])
    type = models.CharField(_('type'), max_length=20, choices=FilmType.choices)
    genres = models.ManyToManyField('Genre', through='GenreFilmwork')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('movie')
        verbose_name_plural = _('movies')


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created_at = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(
                fields=['film_work', 'genre'],
                name='film_work_genre_idx'
            ),
        ]
        db_table = "content\".\"genre_film_work"
        verbose_name = _('movie genre')
        verbose_name_plural = _('movie genres')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField('full name', max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person')
        verbose_name_plural = _('persons')


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.TextField(_('role'), null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(
                fields=['film_work', 'person', 'role'],
                name='film_work_person_idx'
            ),
        ]
        db_table = "content\".\"person_film_work"
        verbose_name = _('actors')
