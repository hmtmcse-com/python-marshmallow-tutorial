from dataclasses import dataclass
from datetime import datetime
from pprint import pprint
from marshmallow import Schema, fields, EXCLUDE


@dataclass
class Example:
    isActive: bool
    name: str
    email: str
    age: int
    salary: float
    houseRent: float
    foodCost: float
    dateOfBirth: datetime
    checkIn: datetime
    officeTime: datetime
    otherDetails: dict
    certificates: list
    identity: str
    isUnder18: bool
    lastAccess: str
    webAddress: str
    uuid: str

    def __init__(
            self,
            name: str,
            isActive: bool = None,
            email: str = None,
            age: int = None,
            salary: float = None,
            houseRent: float = None,
            foodCost: float = None,
            dateOfBirth: datetime = None,
            checkIn: datetime = None,
            officeTime: datetime = None,
            otherDetails: dict = None,
            certificates: list = None,
            identity: str = None,
            isUnder18: bool = None,
            lastAccess: str = None,
            webAddress: str = None,
            uuid: str = None
    ):
        self.isActive = isActive
        self.name = name
        self.email = email
        self.age = age
        self.salary = salary
        self.houseRent = houseRent
        self.foodCost = foodCost
        self.dateOfBirth = dateOfBirth
        self.officeTime = officeTime
        self.checkIn = checkIn
        self.otherDetails = otherDetails
        self.certificates = certificates
        self.identity = identity
        self.isUnder18 = isUnder18
        self.lastAccess = lastAccess
        self.webAddress = webAddress
        self.uuid = uuid


class ExampleSchema(Schema):
    isActive = fields.Boolean(required=True, error_messages={"required": "Please check active."})
    name = fields.String(required=True, error_messages={"required": "Please enter name."})
    email = fields.Email()
    age = fields.Integer(required=True, error_messages={"required": "Please enter age."})
    salary = fields.Number()
    houseRent = fields.Float()
    foodCost = fields.Number()
    dateOfBirth = fields.Date(format="%d-%m-%Y")
    officeTime = fields.Time(format="%H:%M:%S")
    checkIn = fields.DateTime(format="%d-%m-%Y %H:%M:%S")
    otherDetails = fields.Dict(keys=fields.String(), values=fields.String(), required=False)
    certificates = fields.List(fields.String)
    identity = fields.Function(lambda data: data.name.replace(" ", "-").lower() + "-something")
    isUnder18 = fields.Method("is_under_18")
    lastAccess = fields.String()
    webAddress = fields.URL()
    uuid = fields.UUID()

    def is_under_18(self, data):
        if data.age < 18:
            return True
        return False


def get_example_object():
    example = Example("HMTMCSE Education", email="hmtmcse.com@gmail.com", age=7, salary=10, houseRent=50, foodCost=20.10)
    example.dateOfBirth = datetime.strptime("2014-11-21", "%Y-%m-%d")
    example.officeTime = datetime.strptime("13:10:00", "%H:%M:%S")
    example.checkIn = datetime.strptime("2021-12-27 13:10:00", "%Y-%m-%d %H:%M:%S")
    example.otherDetails = {"web": "python", "database": "MariaDB"}
    example.certificates = ["Bsc in CSE"]
    example.lastAccess = "192.168.12.12"
    example.webAddress = "https://www.hmtmcse.com/"
    example.uuid = "123456789"
    example.isActive = False
    return example


def schema_params_dump_test():
    example_dump = get_example_object()
    example_schema_dump = ExampleSchema(unknown=EXCLUDE)
    dump_object = example_schema_dump.dump(example_dump)
    pprint(dump_object)


def deserialization():
    json_string = '{"name": "HMTMCSE Education", "age": 7, "email": "hmtmcse.com@gmail.com", "isActive": false}'
    example = ExampleSchema().loads(json_string)
    print(example)


class MetaDataClass:
    name: str
    email: str


class MetaSchemaClass:
    name = fields.String(required=True, error_messages={"required": "Please enter name."})
    email = fields.Email()

    class Meta:
        exclude = ("email",)


if __name__ == '__main__':
    example = get_example_object()
    example_schema = ExampleSchema()
    dump_object = example_schema.dump(example)
    pprint(dump_object)
