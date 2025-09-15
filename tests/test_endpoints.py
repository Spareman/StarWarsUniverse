import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app, normalize_pagination_params
import app.schemas as schemas
from .fixtures.test_data import TEST_FILMS, TEST_CHARACTERS, TEST_STARSHIPS


class TestStarWarsAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_normalize_pagination_params(self):
        self.assertEqual(normalize_pagination_params(0, 0), (1, 1))
        self.assertEqual(normalize_pagination_params(1, 200), (1, 100))
        self.assertEqual(normalize_pagination_params(5, 20), (5, 20))

    @patch('app.main.logic')
    def test_create_all(self, mock_logic):
        mock_logic.fetch_store_all_data.return_value = [schemas.Film(**film) for film in TEST_FILMS]
        response = self.client.post("/store/all/")
        self.assertEqual(response.status_code, 200)
        films = response.json()
        self.assertIsInstance(films, list)
        self.assertGreater(len(films), 0)

    @patch('app.main.logic')
    def test_create_films(self, mock_logic):
        mock_logic.fetch_store_films.return_value = [schemas.Film(**film) for film in TEST_FILMS]
        response = self.client.post("/store/films/")
        self.assertEqual(response.status_code, 200)
        films = response.json()
        self.assertIsInstance(films, list)
        self.assertGreater(len(films), 0)

    @patch('app.main.logic')
    def test_create_characters(self, mock_logic):
        mock_logic.fetch_store_characters.return_value = [schemas.Character(**char) for char in TEST_CHARACTERS]
        response = self.client.post("/store/characters/")
        self.assertEqual(response.status_code, 200)
        characters = response.json()
        self.assertIsInstance(characters, list)
        self.assertGreater(len(characters), 0)

    @patch('app.main.logic')
    def test_create_starships(self, mock_logic):
        mock_logic.fetch_store_starships.return_value = [schemas.Starship(**ship) for ship in TEST_STARSHIPS]
        response = self.client.post("/store/starships/")
        self.assertEqual(response.status_code, 200)
        starships = response.json()
        self.assertIsInstance(starships, list)
        self.assertGreater(len(starships), 0)

    @patch('app.main.logic')
    def test_read_films(self, mock_logic):
        mock_logic.get_stored_films.return_value = {
            "total": len(TEST_FILMS),
            "page": 1,
            "page_size": 5,
            "total_pages": 1,
            "films": [schemas.Film(**film) for film in TEST_FILMS]
        }
        response = self.client.get("/films/?page=1&page_size=5")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("total", data)
        self.assertIn("page", data)
        self.assertIn("page_size", data)
        self.assertIn("total_pages", data)
        self.assertIn("films", data)
        self.assertIsInstance(data["films"], list)
        self.assertLessEqual(len(data["films"]), 5)

    @patch('app.main.logic')
    def test_read_characters(self, mock_logic):
        mock_logic.get_stored_characters.return_value = {
            "total": len(TEST_CHARACTERS),
            "page": 1,
            "page_size": 5,
            "total_pages": 1,
            "characters": [schemas.Character(**char) for char in TEST_CHARACTERS]
        }
        response = self.client.get("/characters/?page=1&page_size=5")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("total", data)
        self.assertIn("page", data)
        self.assertIn("page_size", data)
        self.assertIn("total_pages", data)
        self.assertIn("characters", data)
        self.assertIsInstance(data["characters"], list)
        self.assertLessEqual(len(data["characters"]), 5)

    @patch('app.main.logic')
    def test_read_starships(self, mock_logic):
        mock_logic.get_stored_starships.return_value = {
            "total": len(TEST_STARSHIPS),
            "page": 1,
            "page_size": 5,
            "total_pages": 1,
            "starships": [schemas.Starship(**ship) for ship in TEST_STARSHIPS]
        }
        response = self.client.get("/starships/?page=1&page_size=5")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("total", data)
        self.assertIn("page", data)
        self.assertIn("page_size", data)
        self.assertIn("total_pages", data)
        self.assertIn("starships", data)
        self.assertIsInstance(data["starships"], list)
        self.assertLessEqual(len(data["starships"]), 5)

    @patch('app.main.logic')
    def test_search_film_by_name(self, mock_logic):
        film_name = "A New Hope"
        mock_logic.search_film_by_name.return_value = schemas.Film(**TEST_FILMS[0])
        response = self.client.get(f"/search/films/?film_name={film_name}")
        film = response.json()
        self.assertIn(film_name.lower(), film["title"].lower())

    @patch('app.main.logic')
    def test_search_film_by_name_bad(self, mock_logic):
        film_name = "wrong"
        mock_logic.search_film_by_name.return_value = None
        response = self.client.get(f"/search/films/?film_name={film_name}")
        self.assertEqual(response.status_code, 404)

    @patch('app.main.logic')
    def test_search_character_by_name(self, mock_logic):
        character_name = "Luke Skywalker"
        mock_logic.search_character_by_name.return_value = schemas.Character(**TEST_CHARACTERS[0])
        response = self.client.get(f"/search/characters/?character_name={character_name}")
        character = response.json()
        self.assertIn(character_name.lower(), character["name"].lower())

    @patch('app.main.logic')
    def test_search_character_by_name_bad(self, mock_logic):
        character_name = "wrong"
        mock_logic.search_character_by_name.return_value = None
        response = self.client.get(f"/search/characters/?character_name={character_name}")
        self.assertEqual(response.status_code, 404)

    @patch('app.main.logic')
    def test_search_starship_by_name(self, mock_logic):
        starship_name = "X-wing"
        mock_logic.search_starship_by_name.return_value = schemas.Starship(**TEST_STARSHIPS[0])
        response = self.client.get(f"/search/starships/?starship_name={starship_name}")
        starship = response.json()
        self.assertIn(starship_name.lower(), starship["name"].lower())

    @patch('app.main.logic')
    def test_search_starship_by_name_bad(self, mock_logic):
        starship_name = "wrong"
        mock_logic.search_starship_by_name.return_value = None
        response = self.client.get(f"/search/starships/?starship_name={starship_name}")
        self.assertEqual(response.status_code, 404)