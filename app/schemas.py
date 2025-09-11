from pydantic import BaseModel

class Character(BaseModel):
    name: str
    age: int
    role: str


class Film(BaseModel):
    title: str
    year: int
    characters: list[Character]

class Starship(BaseModel):
    name: str
    model: str
