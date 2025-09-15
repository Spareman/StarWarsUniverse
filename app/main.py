from fastapi import FastAPI, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
import requests

from .database import SessionLocal, engine
from . import models, schemas, logic


models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="StarWarsUniverse", description="All about Star Wars films, characters, and starships in one place.")
logic = logic.StarWarsLogic()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def normalize_pagination_params(page, page_size):
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 1
    if page_size > 100:
        page_size = 100
    return page, page_size

@app.post("/store/films/", response_model=List[schemas.Film])
def create_films(db: Session = Depends(get_db)):
    try:
        films = logic.fetch_store_films(db)
        return films
    except requests.HTTPError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/store/characters/", response_model=List[schemas.Character])
def create_characters(db: Session = Depends(get_db)):
    try:
        characters = logic.fetch_store_characters(db)
        return characters
    except requests.HTTPError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/store/starships/", response_model=List[schemas.Starship])
def create_starships(db: Session = Depends(get_db)):
    try:
        starships = logic.fetch_store_starships(db)
        return starships
    except requests.HTTPError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/store/all/", response_model=List[schemas.Film])
def create_all(db: Session = Depends(get_db)):
    try:
        films = logic.fetch_store_all_data(db)
        return films
    except requests.HTTPError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/films/", response_model=schemas.PaginatedFilms)
def read_films(
        page: Optional[int] = Query(1, description="Page number for pagination"),
        page_size: Optional[int] = Query(20, description="Number of films per page"),
        db: Session = Depends(get_db)):
    page, page_size = normalize_pagination_params(page, page_size)
    response = logic.get_stored_films(db, page, page_size)
    return response

@app.get("/characters/", response_model=schemas.PaginatedCharacters)
def read_characters(
        page: Optional[int] = Query(1, description="Page number for pagination"),
        page_size: Optional[int] = Query(20, description="Number of characters per page"),
        db: Session = Depends(get_db)):
    page, page_size = normalize_pagination_params(page, page_size)
    response = logic.get_stored_characters(db, page, page_size)
    return response

@app.get("/starships/", response_model=schemas.PaginatedStarships)
def read_starships(
        page: Optional[int] = Query(1, description="Page number for pagination"),
        page_size: Optional[int] = Query(20, description="Number of starships per page"),
        db: Session = Depends(get_db)):
    page, page_size = normalize_pagination_params(page, page_size)
    response = logic.get_stored_starships(db, page, page_size)
    return response

@app.get("/search/films/", response_model=schemas.Film)
def search_film_by_name(film_name: str = Query(None, description="Name of the film to fetch"),
                        db: Session = Depends(get_db)):
    film = logic.search_film_by_name(db, film_name)
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    return film

@app.get("/search/characters/", response_model=schemas.Character)
def search_character_by_name(character_name: str = Query(None, description="Name of the character to fetch"),
                             db: Session = Depends(get_db)):
    character = logic.search_character_by_name(db, character_name)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

@app.get("/search/starships/", response_model=schemas.Starship)
def search_starship_by_name(starship_name: str = Query(None, description="Name of the starship to fetch"),
                            db: Session = Depends(get_db)):
    starship = logic.search_starship_by_name(db, starship_name)
    if not starship:
        raise HTTPException(status_code=404, detail="Starship not found")
    return starship

