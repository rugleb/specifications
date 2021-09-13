from dataclasses import dataclass
from datetime import timedelta
from enum import Enum, unique
from typing import Final, FrozenSet

import specifications


@dataclass(frozen=True)
class Movie:

    @unique
    class Genre(str, Enum):
        ACTION = "action"
        ADVENTURE = "adventure"
        CRIME = "crime"
        DRAMA = "drama"
        FANTASY = "fantasy"
        MYSTERY = "mystery"
        THRILLER = "thriller"
        WESTERN = "western"

    name: str
    directed_by: str
    duration: timedelta
    genres: FrozenSet[Genre]
    rating: float


MOVIES: Final = (
    PULP_FICTION := Movie(
        name="Pulp Fiction",
        directed_by="Quentin Tarantino",
        duration=timedelta(minutes=154),
        genres=frozenset({
            Movie.Genre.CRIME,
            Movie.Genre.DRAMA,
            Movie.Genre.MYSTERY,
        }),
        rating=8.9,
    ),
    HATEFUL_EIGHT := Movie(
        name="The Hateful Eight",
        directed_by="Quentin Tarantino",
        duration=timedelta(minutes=168),
        genres=frozenset({
            Movie.Genre.CRIME,
            Movie.Genre.DRAMA,
            Movie.Genre.MYSTERY,
            Movie.Genre.THRILLER,
            Movie.Genre.WESTERN,
        }),
        rating=7.8,
    ),
    GODFATHER := Movie(
        name="The Godfather",
        directed_by="Francis Ford Coppola",
        duration=timedelta(minutes=177),
        genres=frozenset({
            Movie.Genre.CRIME,
            Movie.Genre.DRAMA,
        }),
        rating=9.2,
    ),
    INCEPTION := Movie(
        name="Inception",
        directed_by="Christopher Nolan",
        duration=timedelta(minutes=148),
        genres=frozenset({
            Movie.Genre.ACTION,
            Movie.Genre.ADVENTURE,
            Movie.Genre.THRILLER,
        }),
        rating=8.8,
    ),
    FIGHT_CLUB := Movie(
        name="Fight Club",
        directed_by="David Fincher",
        duration=timedelta(minutes=139),
        genres=frozenset({
            Movie.Genre.DRAMA,
        }),
        rating=8.8,
    ),
    INTERSTELLAR := Movie(
        name="Interstellar",
        directed_by="Christopher Nolan",
        duration=timedelta(minutes=169),
        genres=frozenset({
            Movie.Genre.ADVENTURE,
            Movie.Genre.DRAMA,
        }),
        rating=8.6,
    ),
    DJANGO_UNCHAINED := Movie(
        name="Django Unchained",
        directed_by="Quentin Tarantino",
        duration=timedelta(minutes=165),
        genres=frozenset({
            Movie.Genre.DRAMA,
            Movie.Genre.WESTERN,
        }),
        rating=8.4,
    ),
)


@dataclass(frozen=True)
class MovieMaxDurationSpecification(specifications.Specification):
    _max_duration: timedelta

    def is_specified_by(self, candidate: Movie) -> bool:
        return candidate.duration < self._max_duration


@dataclass(frozen=True)
class MovieGenreSpecification(specifications.Specification):
    _genre: Movie.Genre

    def is_specified_by(self, candidate: Movie) -> bool:
        return self._genre in candidate.genres


@dataclass(frozen=True)
class MovieDirectorSpecification(specifications.Specification):
    _director: str

    def is_specified_by(self, candidate: Movie) -> bool:
        return self._director == candidate.directed_by


@dataclass(frozen=True)
class MovieMinRatingSpecification(specifications.Specification):
    _min_rating: float

    def is_specified_by(self, candidate: Movie) -> bool:
        return candidate.rating >= self._min_rating


@dataclass(frozen=True)
class MovieEqualSpecification(specifications.Specification):
    _movie: Movie

    def is_specified_by(self, candidate: Movie) -> bool:
        return candidate == self._movie


def test_specification_builder() -> None:
    # define favorite genres
    crime = MovieGenreSpecification(Movie.Genre.CRIME)
    drama = MovieGenreSpecification(Movie.Genre.DRAMA)
    thriller = MovieGenreSpecification(Movie.Genre.THRILLER)
    western = MovieGenreSpecification(Movie.Genre.WESTERN)
    favorite_genre = crime.or_(drama).or_(thriller).and_not(western)

    # define min rating
    high_rating = MovieMinRatingSpecification(8.8)

    # define already watched movies
    pulp_fiction = MovieEqualSpecification(PULP_FICTION)
    inception = MovieEqualSpecification(FIGHT_CLUB)
    already_watched = pulp_fiction.or_(inception)

    # compile target specification
    amazing_movie = favorite_genre.and_(high_rating).and_not(already_watched)

    assert tuple(amazing_movie.select_specified(MOVIES)) == (
        GODFATHER,
        INCEPTION,
    )
    assert tuple(amazing_movie.invert().select_specified(MOVIES)) == (
        PULP_FICTION,
        HATEFUL_EIGHT,
        FIGHT_CLUB,
        INTERSTELLAR,
        DJANGO_UNCHAINED,
    )
