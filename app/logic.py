from swapi_client import SWAPIClient
from schemas import StarshipCreate, CharacterCreate, FilmCreate
from crud import (insert_films, insert_characters, insert_starships, get_characters, get_starships, get_films,
                  get_film_by_name, get_character_by_name, get_starship_by_name,
                  bulk_insert_movies_characters_starships)

class StarWarsLogic:
    def __init__(self):
        self.client = SWAPIClient()

    def fetch_store_films(self, db):
        """
        Fetches all films from SWAPI and stores them in the database.
        :param db: SQLAlchemy.Session: Database session
        :return:
        List[Film]: List of stored films with nested characters and starships
        """
        films = self.client.get_films()
        films_data = [FilmCreate(**film) for film in films]
        stored_films = insert_films(db, films_data)
        return stored_films

    def fetch_store_characters(self, db):
        """
        Fetches all characters from SWAPI and stores them in the database.
        :param db: SQLAlchemy.Session: Database session
        :return:
        List[Character]: List of stored characters with nested starships
        """
        characters = self.client.get_characters()
        characters_data = [CharacterCreate(**char) for char in characters]
        stored_characters = insert_characters(db, characters_data)
        return stored_characters

    def fetch_store_starships(self, db):
        """
        Fetches all starships from SWAPI and stores them in the database.
        :param db: SQLAlchemy.Session: Database session
        :return:
        List[Starship]: List of stored starships
        """
        starships = self.client.get_starships()
        starships_data = [StarshipCreate(**ship) for ship in starships]
        stored_starships = insert_starships(db, starships_data)
        return stored_starships

    def fetch_store_all_data(self, db):
        """
        Fetches all films, characters, and starships from SWAPI and stores them in the database.
        :param db: SQLAlchemy.Session: Database session
        :return:
        List[Film]: List of stored films with nested characters and starships
        """
        films = self.client.get_films()
        characters = self.client.get_characters()
        starships = self.client.get_starships()

        starships_data = [StarshipCreate(**ship) for ship in starships]
        characters_data = [CharacterCreate(**char) for char in characters]
        films_data = [FilmCreate(**film) for film in films]

        stored_films = bulk_insert_movies_characters_starships(db, films_data, characters_data, starships_data)

        return stored_films

    @staticmethod
    def get_stored_films(db, page=1, page_size=20):
        """
        Fetches films from the database.
        :param db: SQLAlchemy.Session: Database session
        :param page: int: Page number for pagination
        :param page_size: int: Number of films per page
        :return:
        List[Film]: List of all films with nested characters and starships
        """
        skip = (page - 1) * page_size
        total, films = get_films(db, skip, page_size)
        total_pages = (total + page_size - 1) // page_size
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "films": films
        }

    @staticmethod
    def get_stored_characters(db, page=1, page_size=20):
        """
        Fetches characters from the database.
        :param db: SQLAlchemy.Session: Database session
        :param page: int: Page number for pagination
        :param page_size: int: Number of characters per page
        :return:
        List[Character]: List of all characters with nested starships
        """
        skip = (page - 1) * page_size
        total, characters = get_characters(db, skip, page_size)
        total_pages = (total + page_size - 1) // page_size
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "characters": characters
        }

    @staticmethod
    def get_stored_starships(db, page=1, page_size=20):
        """
        Fetches starships from the database.
        :param db: SQLAlchemy.Session: Database session
        :param page: int: Page number for pagination
        :param page_size: int: Number of starships per page
        :return:
        List[Starship]: List of all starships
        """
        skip = (page - 1) * page_size
        total, starships = get_starships(db, skip, page_size)
        total_pages = (total + page_size - 1) // page_size
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "starships": starships
        }

    @staticmethod
    def search_film_by_name(db, film_name):
        """
        Fetches a film by name from the database.
        :param db: SQLAlchemy.Session: Database session
        :param film_name: str: Name of the film to fetch
        :return:
        Film: The fetched film with nested characters and starships
        """
        return get_film_by_name(db, film_name)

    @staticmethod
    def search_character_by_name(db, character_name):
        """
        Fetches a character by name from the database.
        :param db: SQLAlchemy.Session: Database session
        :param character_name: str: Name of the character to fetch
        :return:
        Character: The fetched character with nested starships
        """
        return get_character_by_name(db, character_name)

    @staticmethod
    def search_starship_by_name(db, starship_name):
        """
        Fetches a starship by name from the database.
        :param db: SQLAlchemy.Session: Database session
        :param starship_name: str: Name of the starship to fetch
        :return:
        Starship: The fetched starship
        """
        return get_starship_by_name(db, starship_name)