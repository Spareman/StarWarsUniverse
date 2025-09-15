import unittest
from unittest.mock import patch, MagicMock
from app.logic import StarWarsLogic

class TestStarWarsLogic(unittest.TestCase):

    @patch('app.logic.SWAPIClient')
    @patch('app.logic.insert_films')
    def test_fetch_store_films(self, mock_insert_films, mock_swapi_client):

        mock_swapi_client_instance = mock_swapi_client.return_value
        mock_swapi_client_instance.get_films.return_value = [
            {
                "title": "A New Hope",
                "episode_id": 4,
                "opening_crawl": "It is a period of civil war...",
                "director": "George Lucas",
                "producer": "Gary Kurtz, Rick McCallum",
                "release_date": "1977-05-25",
                "characters": ["http://swapi.dev/api/people/1/"],
                "starships": ["http://swapi.dev/api/starships/2/"],
                "created": "2014-12-10T14:23:31.880000Z",
                "edited": "2014-12-20T19:49:45.256000Z",
                "url": "http://swapi.dev/api/films/1/"
            }
        ]

        mock_insert_films.return_value = ["mocked_film"]

        logic = StarWarsLogic()
        db_mock = MagicMock()
        result = logic.fetch_store_films(db_mock)

        self.assertEqual(result, ["mocked_film"])
        mock_swapi_client_instance.get_films.assert_called_once()
        mock_insert_films.assert_called_once()
        args, kwargs = mock_insert_films.call_args
        self.assertEqual(args[0], db_mock)
        self.assertEqual(len(args[1]), 1)

    @patch('app.logic.SWAPIClient')
    @patch('app.logic.insert_characters')
    def test_fetch_store_characters(self, mock_insert_characters, mock_swapi_client):

        mock_swapi_client_instance = mock_swapi_client.return_value
        mock_swapi_client_instance.get_characters.return_value = [
            {
                "name": "Luke Skywalker",
                "height": "172",
                "mass": "77",
                "hair_color": "blond",
                "skin_color": "fair",
                "eye_color": "blue",
                "birth_year": "19BBY",
                "gender": "male",
                "homeworld": "https://swapi.info/api/planets/1",
                "films": ["https://swapi.info/api/films/1"],
                "species": [],
                "vehicles": ["https://swapi.info/api/vehicles/14"],
                "starships": ["https://swapi.info/api/starships/12"],
                "created": "2014-12-09T13:50:51.644000Z",
                "edited": "2014-12-20T21:17:56.891000Z",
                "url": "https://swapi.info/api/people/1"
            }
        ]
        mock_insert_characters.return_value = ["mocked_character"]
        logic = StarWarsLogic()
        db_mock = MagicMock()
        result = logic.fetch_store_characters(db_mock)
        self.assertEqual(result, ["mocked_character"])
        mock_swapi_client_instance.get_characters.assert_called_once()
        mock_insert_characters.assert_called_once()
        args, kwargs = mock_insert_characters.call_args
        self.assertEqual(args[0], db_mock)
        self.assertEqual(len(args[1]), 1)

    @patch('app.logic.SWAPIClient')
    @patch('app.logic.insert_starships')
    def test_fetch_store_starships(self, mock_insert_starships, mock_swapi_client):

        mock_swapi_client_instance = mock_swapi_client.return_value
        mock_swapi_client_instance.get_starships.return_value = [
            {
                "name": "X-wing",
                "model": "T-65 X-wing",
                "manufacturer": "Incom Corporation",
                "cost_in_credits": "149999",
                "length": "12.5",
                "max_atmosphering_speed": "1050",
                "crew": "1",
                "passengers": "0",
                "cargo_capacity": "110",
                "consumables": "1 week",
                "hyperdrive_rating": "1.0",
                "MGLT": "100",
                "starship_class": "Starfighter",
                "pilots": [
                    "https://swapi.info/api/people/1/",
                    "https://swapi.info/api/people/9/"
                ],
                "films": [
                    "https://swapi.info/api/films/1/",
                    "https://swapi.info/api/films/2/"
                ],
                "created": "2014-12-12T11:19:05.340000Z",
                "edited": "2014-12-20T21:23:49.886000Z",
                "url": "https://swapi.info/api/starships/12/"
            }
        ]
        mock_insert_starships.return_value = ["mocked_starship"]
        logic = StarWarsLogic()
        db_mock = MagicMock()
        result = logic.fetch_store_starships(db_mock)
        self.assertEqual(result, ["mocked_starship"])
        mock_swapi_client_instance.get_starships.assert_called_once()
        mock_insert_starships.assert_called_once()
        args, kwargs = mock_insert_starships.call_args
        self.assertEqual(args[0], db_mock)
        self.assertEqual(len(args[1]), 1)

    @patch('app.logic.SWAPIClient')
    @patch('app.logic.bulk_insert_movies_characters_starships')
    def test_fetch_store_all_data(self, mock_bulk_insert, mock_swapi_client):

        mock_swapi_client_instance = mock_swapi_client.return_value
        mock_swapi_client_instance.get_films.return_value = [
            {
                "title": "A New Hope",
                "episode_id": 4,
                "opening_crawl": "It is a period of civil war...",
                "director": "George Lucas",
                "producer": "Gary Kurtz, Rick McCallum",
                "release_date": "1977-05-25",
                "characters": ["http://swapi.dev/api/people/1/"],
                "starships": ["http://swapi.dev/api/starships/2/"],
                "created": "2014-12-10T14:23:31.880000Z",
                "edited": "2014-12-20T19:49:45.256000Z",
                "url": "http://swapi.dev/api/films/1/"
            }
        ]
        mock_swapi_client_instance.get_characters.return_value =  [
            {
                "name": "Luke Skywalker",
                "height": "172",
                "mass": "77",
                "hair_color": "blond",
                "skin_color": "fair",
                "eye_color": "blue",
                "birth_year": "19BBY",
                "gender": "male",
                "homeworld": "https://swapi.info/api/planets/1",
                "films": ["https://swapi.info/api/films/1"],
                "species": [],
                "vehicles": ["https://swapi.info/api/vehicles/14"],
                "starships": ["https://swapi.info/api/starships/12"],
                "created": "2014-12-09T13:50:51.644000Z",
                "edited": "2014-12-20T21:17:56.891000Z",
                "url": "https://swapi.info/api/people/1"
            }
        ]
        mock_swapi_client_instance.get_starships.return_value = [
            {
                "name": "X-wing",
                "model": "T-65 X-wing",
                "manufacturer": "Incom Corporation",
                "cost_in_credits": "149999",
                "length": "12.5",
                "max_atmosphering_speed": "1050",
                "crew": "1",
                "passengers": "0",
                "cargo_capacity": "110",
                "consumables": "1 week",
                "hyperdrive_rating": "1.0",
                "MGLT": "100",
                "starship_class": "Starfighter",
                "pilots": [
                    "https://swapi.info/api/people/1/",
                    "https://swapi.info/api/people/9/"
                ],
                "films": [
                    "https://swapi.info/api/films/1/",
                    "https://swapi.info/api/films/2/"
                ],
                "created": "2014-12-12T11:19:05.340000Z",
                "edited": "2014-12-20T21:23:49.886000Z",
                "url": "https://swapi.info/api/starships/12/"
            }
        ]
        mock_bulk_insert.return_value = ["mocked_bulk_insert_result"]
        logic = StarWarsLogic()
        db_mock = MagicMock()
        result = logic.fetch_store_all_data(db_mock)
        self.assertEqual(result, ["mocked_bulk_insert_result"])
        mock_swapi_client_instance.get_films.assert_called_once()
        mock_swapi_client_instance.get_characters.assert_called_once()
        mock_swapi_client_instance.get_starships.assert_called_once()
        mock_bulk_insert.assert_called_once()
        args, kwargs = mock_bulk_insert.call_args
        self.assertEqual(args[0], db_mock)
        self.assertEqual(len(args[1]), 1)
        self.assertEqual(len(args[2]), 1)
        self.assertEqual(len(args[3]), 1)

    @patch('app.logic.get_films')
    def test_get_stored_films(self, mock_get_films):
        mock_get_films.return_value = 2, ["film1", "film2"]
        logic = StarWarsLogic()
        db_mock = MagicMock()
        expected_result = {
            "total": 2,
            "page": 1,
            "page_size": 20,
            "total_pages": 1,
            "films": ["film1", "film2"]
        }
        result = logic.get_stored_films(db_mock)
        self.assertEqual(result, expected_result)
        mock_get_films.assert_called_once_with(db_mock, 0, 20)

    @patch('app.logic.get_characters')
    def test_get_stored_characters(self, mock_get_characters):
        mock_get_characters.return_value = 3, ["char1", "char2", "char3"]
        logic = StarWarsLogic()
        db_mock = MagicMock()
        expected_result = {
            "total": 3,
            "page": 1,
            "page_size": 20,
            "total_pages": 1,
            "characters": ["char1", "char2", "char3"]
        }
        result = logic.get_stored_characters(db_mock)
        self.assertEqual(result, expected_result)
        mock_get_characters.assert_called_once_with(db_mock, 0, 20)

    @patch('app.logic.get_starships')
    def test_get_stored_starships(self, mock_get_starships):
        mock_get_starships.return_value = 4, ["ship1", "ship2", "ship3", "ship4"]
        logic = StarWarsLogic()
        db_mock = MagicMock()
        expected_result = {
            "total": 4,
            "page": 1,
            "page_size": 20,
            "total_pages": 1,
            "starships": ["ship1", "ship2", "ship3", "ship4"]
        }
        result = logic.get_stored_starships(db_mock)
        self.assertEqual(result, expected_result)
        mock_get_starships.assert_called_once_with(db_mock, 0, 20)

    @patch('app.logic.get_film_by_name')
    def test_search_film_by_name(self, mock_get_film_by_name):
        mock_get_film_by_name.return_value = "mocked_film"
        logic = StarWarsLogic()
        db_mock = MagicMock()
        result = logic.search_film_by_name(db_mock, "A New Hope")
        self.assertEqual(result, "mocked_film")
        mock_get_film_by_name.assert_called_once_with(db_mock, "A New Hope")

    @patch('app.logic.get_film_by_name')
    def test_search_film_by_name_not_found(self, mock_get_film_by_name):
        mock_get_film_by_name.return_value = None
        logic = StarWarsLogic()
        db_mock = MagicMock()
        result = logic.search_film_by_name(db_mock, "Nonexistent Film")
        self.assertIsNone(result)
        mock_get_film_by_name.assert_called_once_with(db_mock, "Nonexistent Film")

    @patch('app.logic.get_character_by_name')
    def test_search_character_by_name(self, mock_get_character_by_name):
        mock_get_character_by_name.return_value = "mocked_character"
        logic = StarWarsLogic()
        db_mock = MagicMock()
        result = logic.search_character_by_name(db_mock, "Luke Skywalker")
        self.assertEqual(result, "mocked_character")
        mock_get_character_by_name.assert_called_once_with(db_mock, "Luke Skywalker")

    @patch('app.logic.get_character_by_name')
    def test_search_character_by_name_not_found(self, mock_get_character_by_name):
        mock_get_character_by_name.return_value = None
        logic = StarWarsLogic()
        db_mock = MagicMock()
        result = logic.search_character_by_name(db_mock, "Nonexistent Character")
        self.assertIsNone(result)
        mock_get_character_by_name.assert_called_once_with(db_mock, "Nonexistent Character")

    @patch('app.logic.get_starship_by_name')
    def test_search_starship_by_name(self, mock_get_starship_by_name):
        mock_get_starship_by_name.return_value = "mocked_starship"
        logic = StarWarsLogic()
        db_mock = MagicMock()
        result = logic.search_starship_by_name(db_mock, "X-wing")
        self.assertEqual(result, "mocked_starship")
        mock_get_starship_by_name.assert_called_once_with(db_mock, "X-wing")

    @patch('app.logic.get_starship_by_name')
    def test_search_starship_by_name_not_found(self, mock_get_starship_by_name):
        mock_get_starship_by_name.return_value = None
        logic = StarWarsLogic()
        db_mock = MagicMock()
        result = logic.search_starship_by_name(db_mock, "Nonexistent Starship")
        self.assertIsNone(result)
        mock_get_starship_by_name.assert_called_once_with(db_mock, "Nonexistent Starship")
