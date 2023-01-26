import uuid
from typing import Optional
from datetime import datetime, timezone
from dataclasses import dataclass, field


@dataclass
class FilmWork:
    type: str
    title: str
    file_path: Optional[str]
    description: Optional[str]
    creation_date: Optional[str]
    rating: float = field(default=0.0)
    created_at: str = datetime.now(timezone.utc)
    updated_at: str = datetime.now(timezone.utc)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Genre:
    name: str
    description: str
    created_at: str = datetime.now(timezone.utc)
    updated_at: str = datetime.now(timezone.utc)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Person:
    full_name: str
    created_at: str = datetime.now(timezone.utc)
    updated_at: str = datetime.now(timezone.utc)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class PersonFilmWork:
    role: str
    person_id: uuid.UUID
    film_work_id: uuid.UUID
    created_at: str = datetime.now(timezone.utc)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class GenreFilmWork:
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: str = datetime.now(timezone.utc)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
