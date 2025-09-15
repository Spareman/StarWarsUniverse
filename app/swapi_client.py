import requests

class SWAPIClient:
    def __init__(self):
        self.base_url = "https://swapi.info/api/"

    def get_films(self, film_id=None):
        film_id = "" if film_id is None else film_id
        response = requests.get(f"{self.base_url}films/{film_id}")
        response.raise_for_status()
        return response.json()

    def get_characters(self, character_id=None):
        character_id = "" if character_id is None else character_id
        response = requests.get(f"{self.base_url}people/{character_id}")
        response.raise_for_status()
        return response.json()

    def get_starships(self, starship_id=None):
        starship_id = "" if starship_id is None else starship_id
        response = requests.get(f"{self.base_url}starships/{starship_id}")
        response.raise_for_status()
        return response.json()
