import unittest
from unittest.mock import patch

from app.swapi_client import SWAPIClient

class TestSWAPIClient(unittest.TestCase):

    @patch('app.swapi_client.requests.get')
    def test_get_films(self, mock_get):
        mock_response = [
                {
                    "title": "A New Hope",
                    "episode_id": 4,
                    "opening_crawl": "It is a period of civil war....",
                    "director": "George Lucas",
                    "producer": "Gary Kurtz, Rick McCallum",
                    "release_date": "1977-05-25",
                    "characters": [
                        "https://swapi.info/api/people/1/",
                        "https://swapi.info/api/people/2/"
                    ],
                    "planets": [
                        "https://swapi.info/api/planets/1/",
                        "https://swapi.info/api/planets/2/"
                    ],
                    "starships": [
                        "https://swapi.info/api/starships/2/",
                        "https://swapi.info/api/starships/3/"
                    ],
                    "vehicles": [
                        "https://swapi.info/api/vehicles/4/",
                        "https://swapi.info/api/vehicles/6/"
                    ],
                    "species": [
                        "https://swapi.info/api/species/1/",
                        "https://swapi.info/api/species/2/"
                    ],
                    "created": "2014-12-10T14:23:31.880000Z",
                    "edited": "2014-12-20T19:49:45.256000Z",
                    "url": "https://swapi.info/api/films/1/"
                }
            ]
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        client = SWAPIClient()
        films = client.get_films()
        self.assertEqual(len(films), 1)
        self.assertEqual(films[0]["title"], "A New Hope")

    @patch('app.swapi_client.requests.get')
    def test_get_characters(self, mock_get):
        mock_response = [
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
                "films": [
                    "https://swapi.info/api/films/1",
                    "https://swapi.info/api/films/2"
                ],
                "species": [],
                "vehicles": [
                    "https://swapi.info/api/vehicles/14",
                    "https://swapi.info/api/vehicles/30"
                ],
                "starships": [
                    "https://swapi.info/api/starships/12",
                    "https://swapi.info/api/starships/22"
                ],
                "created": "2014-12-09T13:50:51.644000Z",
                "edited": "2014-12-20T21:17:56.891000Z",
                "url": "https://swapi.info/api/people/1"
            }
        ]
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        client = SWAPIClient()
        characters = client.get_characters()
        self.assertEqual(len(characters), 1)
        self.assertEqual(characters[0]["name"], "Luke Skywalker")

    @patch('app.swapi_client.requests.get')
    def test_get_starships(self, mock_get):
        mock_response = [
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
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        client = SWAPIClient()
        starships = client.get_starships()
        self.assertEqual(len(starships), 1)
        self.assertEqual(starships[0]["name"], "X-wing")