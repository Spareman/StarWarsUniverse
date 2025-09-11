from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Association tables for many-to-many relationships
films_characters = Table(
    'films_characters', Base.metadata,
    Column('film_id', Integer, ForeignKey('films.id')),
    Column('character_id', Integer, ForeignKey('characters.id'))
)

films_starships = Table(
    'films_starships', Base.metadata,
    Column('film_id', Integer, ForeignKey('films.id')),
    Column('starship_id', Integer, ForeignKey('starships.id'))
)

class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    year = Column(Integer)

    characters = relationship("Character", secondary="films_characters", back_populates="films")
    starships = relationship("Starship", secondary="films_starships", back_populates="films")

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    role = Column(String)
    film_id = Column(Integer, ForeignKey("films.id"))

    films = relationship("Film", secondary="films_characters", back_populates="characters")

class Starship(Base):
    __tablename__ = "starships"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    model = Column(String)

    films = relationship("Film", secondary="films_starships", back_populates="starships")
