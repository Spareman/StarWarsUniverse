from pydantic import BaseModel
from typing import List
from datetime import datetime

class FilmBase(BaseModel):
    title: str
    episode_id: int
    opening_crawl: str
    director: str
    producer: str
    release_date: str

class CharacterBase(BaseModel):
    name: str
    height: str
    mass: str
    hair_color: str
    skin_color: str
    eye_color: str
    birth_year: str
    gender: str

class StarshipBase(BaseModel):
    name: str
    model: str
    manufacturer: str
    cost_in_credits: str
    length: str
    max_atmosphering_speed: str
    crew: str
    passengers: str
    cargo_capacity: str
    consumables: str
    hyperdrive_rating: str
    MGLT: str
    starship_class: str

class StarshipCreate(StarshipBase):
    url: str

class CharacterCreate(CharacterBase):
    url: str
    starships: List[str] = []

class FilmCreate(FilmBase):
    url: str
    characters: List[str] = []
    starships: List[str] = []

class Starship(StarshipBase):
    id: int
    created_at: datetime
    # url: str

    class Config:
        orm_mode = True

class Character(CharacterBase):
    id: int
    created_at: datetime
    # url: str
    films: List[FilmBase] = []
    starships: List[StarshipBase] = []

    class Config:
        orm_mode = True

class Film(FilmBase):
    id: int
    created_at: datetime
    # url: str
    characters: List[CharacterBase] = []
    starships: List[StarshipBase] = []

    class Config:
        orm_mode = True

class PaginatedFilms(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    films: List[Film]

class PaginatedCharacters(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    characters: List[Character]

class PaginatedStarships(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    starships: List[Starship]
