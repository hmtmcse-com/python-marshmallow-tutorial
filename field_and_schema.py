from dataclasses import dataclass
from pprint import pprint

from marshmallow import Schema, fields, post_load


@dataclass
class Person:
    first_name: str
    last_name: str
    email: str
    age: int
    income: float

    def __init__(self, first_name: str, last_name: str = None, email: str = None, age: int = None, income: float = None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.age = age
        self.income = income


class PersonSchema(Schema):
    first_name = fields.String(required=True, error_messages={"required": "Please enter first name"})
    last_name = fields.String(allow_none=None)
    email = fields.Email(allow_none=None)
    age = fields.Integer(allow_none=None)
    income = fields.Float(allow_none=None)

    @post_load
    def dict_to_object(self, data, **kwargs):
        return Person(**data)


if __name__ == '__main__':
    person = Person(first_name="Touhid", last_name="Mia", email="hmtmcse.com@gmail.com", age=30, income=500)
    person_schema = PersonSchema()
    json_string = person_schema.dump(person)
    pprint(json_string)

    json_dict = {'age': 30, 'email': 'hmtmcse.com@gmail.com', 'first_name': 'Touhid', 'income': 500.0}

    person_object = person_schema.load(json_dict)
    pprint(person_object)
