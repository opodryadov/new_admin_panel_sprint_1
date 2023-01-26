CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NULL,
    creation_date DATE NULL,
    file_path TEXT NULL,
    rating FLOAT NULL,
    type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS content.genre (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NULL
);

CREATE TABLE IF NOT EXISTS content.person (
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    id uuid NOT NULL PRIMARY KEY,
    full_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid NOT NULL PRIMARY KEY,
    role TEXT NULL,
    created_at timestamp with time zone NOT NULL,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid NOT NULL PRIMARY KEY,
    created_at timestamp with time zone NOT NULL,
    film_work_id uuid NOT NULL,
    genre_id uuid NOT NULL
);

CREATE INDEX film_work_person_idx ON content.person_film_work (film_work_id, person_id, role);

CREATE INDEX film_work_genre_idx ON content.genre_film_work (film_work_id, genre_id);

ALTER TABLE content.person_film_work ADD CONSTRAINT fk_film_work_id FOREIGN KEY (film_work_id) REFERENCES content.film_work (id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE content.person_film_work ADD CONSTRAINT fk_person_id FOREIGN KEY (person_id) REFERENCES content.person (id) DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX fk_person_film_work_id ON content.person_film_work (film_work_id);

CREATE INDEX fk_person_person_id ON content.person_film_work (person_id);

ALTER TABLE content.genre_film_work ADD CONSTRAINT fk_film_work_id FOREIGN KEY (film_work_id) REFERENCES content.film_work (id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE content.genre_film_work ADD CONSTRAINT fk_genre_id FOREIGN KEY (genre_id) REFERENCES content.genre (id) DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX fk_genre_film_work_id ON content.genre_film_work (film_work_id);

CREATE INDEX "fk_genre_genre_id" ON content.genre_film_work (genre_id);