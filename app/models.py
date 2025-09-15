from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from database import Base

# Association tables for many-to-many relationships
films_characters = Table(
    'films_characters', Base.metadata,
    Column('film_id', Integer, ForeignKey('films.id')),
    Column('character_id', Integer, ForeignKey('characters.id')),
    extend_existing=True
)

films_starships = Table(
    'films_starships', Base.metadata,
    Column('film_id', Integer, ForeignKey('films.id')),
    Column('starship_id', Integer, ForeignKey('starships.id')),
    extend_existing=True
)

characters_starships = Table(
    'characters_starships', Base.metadata,
    Column('character_id', Integer, ForeignKey('characters.id')),
    Column('starship_id', Integer, ForeignKey('starships.id')),
    extend_existing=True
)

class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, index=True)
    title = Column(String, index=True)
    episode_id = Column(Integer)
    opening_crawl = Column(String)
    director = Column(String)
    producer = Column(String)
    release_date = Column(String)
    url = Column(String, unique=True, index=True)

    characters = relationship("Character", secondary="films_characters", back_populates="films")
    starships = relationship("Starship", secondary="films_starships", back_populates="films")

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, index=True)
    name = Column(String, index=True)
    height = Column(String)
    mass = Column(String)
    hair_color = Column(String)
    skin_color = Column(String)
    eye_color = Column(String)
    birth_year = Column(String)
    gender = Column(String)
    url = Column(String, unique=True, index=True)

    films = relationship("Film", secondary="films_characters", back_populates="characters")
    starships = relationship("Starship", secondary="characters_starships", back_populates="characters")

class Starship(Base):
    __tablename__ = "starships"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, index=True)
    name = Column(String, index=True)
    model = Column(String)
    manufacturer = Column(String)
    cost_in_credits = Column(String)
    length = Column(String)
    max_atmosphering_speed = Column(String)
    crew = Column(String)
    passengers = Column(String)
    cargo_capacity = Column(String)
    consumables = Column(String)
    hyperdrive_rating = Column(String)
    MGLT = Column(String)
    starship_class = Column(String)
    url = Column(String, unique=True, index=True)

    films = relationship("Film", secondary="films_starships", back_populates="starships")
    characters = relationship("Character", secondary="characters_starships", back_populates="starships")
