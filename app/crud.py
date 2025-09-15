import datetime
import models
from decorators import db_exception_handler
from swapi_client import SWAPIClient
from schemas import StarshipCreate, CharacterCreate, FilmCreate

client = SWAPIClient()

@db_exception_handler
def insert_starships(db, starships_data, check_existing=True):
    """
    Inserts starships into the database.
    :param db: SQLAlchemy.Session: Database session
    :param starships_data: List[StarshipCreate]: List of starship data from SWAPI
    :param check_existing: bool: Whether to check for existing starships to avoid duplicates
    :return:
    List[Starship]: List of stored starships
    """
    if check_existing:
        existing_starships = [r[0] for r in db.query(models.Starship.name).all()]
        starships_data = [ship for ship in starships_data if ship.name not in existing_starships]
    starships = []
    for ship in starships_data:
        db_ship = models.Starship(
            created_at=datetime.datetime.now(),
            name=ship.name,
            model=ship.model,
            manufacturer=ship.manufacturer,
            cost_in_credits=ship.cost_in_credits,
            length=ship.length,
            max_atmosphering_speed=ship.max_atmosphering_speed,
            crew=ship.crew,
            passengers=ship.passengers,
            cargo_capacity=ship.cargo_capacity,
            consumables=ship.consumables,
            hyperdrive_rating=ship.hyperdrive_rating,
            MGLT=ship.MGLT,
            starship_class=ship.starship_class,
            url=ship.url
        )
        starships.append(db_ship)
    if starships:
        db.add_all(starships)
        db.commit()
    return starships

@db_exception_handler
def insert_characters(db, characters_data, check_existing=True):
    """
    Inserts characters into the database.
    :param db: SQLAlchemy.Session: Database session
    :param characters_data: List[CharacterCreate]: List of character data from SWAPI
    :param check_existing: bool: Whether to check for existing characters to avoid duplicates
    :return:
    List[Character]: List of stored characters with nested starships
    """
    if check_existing:
        existing_characters = [r[0] for r in db.query(models.Character.name).all()]
        characters_data = [char for char in characters_data if char.name not in existing_characters]
    characters = []
    for char in characters_data:
        db_char = models.Character(
            created_at=datetime.datetime.now(),
            name=char.name,
            height=char.height,
            mass=char.mass,
            hair_color=char.hair_color,
            skin_color=char.skin_color,
            eye_color=char.eye_color,
            birth_year=char.birth_year,
            gender=char.gender,
            url=char.url
        )
        new_ship_data = []
        for ship in char.starships:
            db_ship = db.query(models.Starship).filter(models.Starship.url == ship).first()
            if db_ship:
                db_char.starships.append(db_ship)
            else:
                ship_id = ship.split("/")[-1]
                new_ship_data.append(StarshipCreate(**client.get_starships(ship_id)))
        if new_ship_data:
            new_ships = insert_starships(db, new_ship_data, False)
            db_char.starships += new_ships
        characters.append(db_char)
    if characters:
        db.add_all(characters)
        db.commit()
    return characters

@db_exception_handler
def insert_films(db, films_data):
    """
    Inserts films into the database.
    :param db: SQLAlchemy.Session: Database session
    :param films_data: List[FilmCreate]: List of film data from SWAPI
    :return:
    List[Film]: List of stored films with nested characters and starships
    """
    existing_films = [r[0] for r in db.query(models.Film.title).all()]
    films_data = [film for film in films_data if film.title not in existing_films]
    films = []
    for film in films_data:
        db_film = models.Film(
            created_at=datetime.datetime.now(),
            title=film.title,
            episode_id=film.episode_id,
            opening_crawl=film.opening_crawl,
            director=film.director,
            producer=film.producer,
            release_date=film.release_date,
            url=film.url
        )
        new_char_data = []
        for char in film.characters:
            db_char = db.query(models.Character).filter(models.Character.url == char).first()
            if db_char:
                db_film.characters.append(db_char)
            else:
                char_id = char.split("/")[-1]
                new_char_data.append(CharacterCreate(**client.get_characters(char_id)))
        if new_char_data:
            new_chars = insert_characters(db, new_char_data, False)
            db_film.characters += new_chars

        new_ship_data = []
        for ship in film.starships:
            db_ship = db.query(models.Starship).filter(models.Starship.url == ship).first()
            if db_ship:
                db_film.starships.append(db_ship)
            else:
                ship_id = ship.split("/")[-1]
                new_ship_data.append(StarshipCreate(**client.get_starships(ship_id)))
        if new_ship_data:
            new_ships = insert_starships(db, new_ship_data, False)
            db_film.starships += new_ships
        films.append(db_film)
    if films:
        db.add_all(films)
        db.commit()
    return films

@db_exception_handler
def bulk_insert_movies_characters_starships(db, films_data, characters_data, starships_data):
    """
    Bulk inserts films, characters, and starships into the database.
    :param db: SQLAlchemy.Session: Database session
    :param films_data: List[FilmCreate]: List of film data from SWAPI
    :param characters_data: List[CharacterCreate]: List of character data from SWAPI
    :param starships_data: List[StarshipCreate]: List of starship data from SWAPI
    :return:
    List[Film]: List of stored films with nested characters and starships
    """

    starships = insert_starships(db, starships_data)

    characters = insert_characters(db, characters_data)

    films = insert_films(db, films_data)

    return films

@db_exception_handler
def get_films(db, skip=0, limit=20):
    """
    Fetches all films from the database.
    :param db: SQLAlchemy.Session: Database session
    :param skip: int: Number of items to skip for pagination
    :param limit: int: Number of items to return for pagination
    :return:
    List[Film]: List of all films with nested characters and starships
    """
    total = db.query(models.Film).count()
    films = db.query(models.Film).offset(skip).limit(limit).all()
    return total, films

@db_exception_handler
def get_characters(db, skip=0, limit=20):
    """
    Fetches all characters from the database.
    :param db: SQLAlchemy.Session: Database session
    :param skip: int: Number of items to skip for pagination
    :param limit: int: Number of items to return for pagination
    :return:
    List[Character]: List of all characters with nested starships
    """
    total = db.query(models.Character).count()
    characters = db.query(models.Character).offset(skip).limit(limit).all()
    return total, characters

@db_exception_handler
def get_starships(db, skip=0, limit=20):
    """
    Fetches all starships from the database.
    :param db: SQLAlchemy.Session: Database session
    :param skip: int: Number of items to skip for pagination
    :param limit: int: Number of items to return for pagination
    :return:
    List[Starship]: List of all starships
    """
    total = db.query(models.Starship).count()
    starships = db.query(models.Starship).offset(skip).limit(limit).all()
    return total, starships

@db_exception_handler
def get_film_by_name(db, film_name):
    """
    Fetches a film by name from the database.
    :param db: SQLAlchemy.Session: Database session
    :param film_name: str: Name of the film to fetch
    :return:
    Film: The fetched film with nested characters and starships
    """
    film = db.query(models.Film).filter(models.Film.title.ilike(f"%{film_name}%")).first()
    return film if isinstance(film, models.Film) else None

@db_exception_handler
def get_character_by_name(db, character_name):
    """
    Fetches a character by name from the database.
    :param db: SQLAlchemy.Session: Database session
    :param character_name: str: Name of the character to fetch
    :return:
    Character: The fetched character with nested starships
    """
    character = db.query(models.Character).filter(models.Character.name.ilike(f"%{character_name}%")).first()
    return character if isinstance(character, models.Character) else None

@db_exception_handler
def get_starship_by_name(db, starship_name):
    """
    Fetches a starship by name from the database.
    :param db: SQLAlchemy.Session: Database session
    :param starship_name: str: Name of the starship to fetch
    :return:
    Starship: The fetched starship
    """
    starship = db.query(models.Starship).filter(models.Starship.name.ilike(f"%{starship_name}%")).first()
    return starship if isinstance(starship, models.Starship) else None
