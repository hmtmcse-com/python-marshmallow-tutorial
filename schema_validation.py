from pprint import pprint
from marshmallow import fields, Schema, ValidationError, validate, validates, validates_schema


class PersonSchema(Schema):
    first_name = fields.String(required=True, error_messages={"required": "Please enter first name"})
    last_name = fields.String(allow_none=None)
    email = fields.Email(required=True, error_messages={"required": "Please enter email."})
    income = fields.Float(allow_none=None)


def handle_validation_error():
    json_string = '{"first_name" : "HMTMCSE", "age" : 7}'
    try:
        person = PersonSchema().loads(json_string)
        pprint(person)
    except ValidationError as error:
        # Print Error Messages
        print("Print Errors: ")
        print(error.messages)

        print("\nValid datas :")
        # Get the valid data
        print(error.valid_data)


def validate_list_of_data():
    input_dict = [
        {"first_name": "HMTMCSE", "email": "hmtmcse@gmail.com"},
        {"last_name": "Education", "email": "hmtmcse@gmail.com"},
        {"last_name": "Education", "email": "hmtmcse@gmail"},
    ]
    try:
        persons = PersonSchema().load(input_dict, many=True)
        pprint(persons)
    except ValidationError as error:
        # Print Error Messages
        print("Print Errors: ")
        print(error.messages)

        print("\nValid datas :")
        # Get the valid data
        print(error.valid_data)


def validate_without_deserialization():
    data = {"last_name": "Education", "email": "hmtmcse@gmail.com"}
    try:
        errors = PersonSchema().validate(data)
        pprint(errors)
    except ValidationError as error:
        # Print Error Messages
        print("Print Errors: ")
        print(error.messages)


class ApplySchemaValidator(Schema):
    permission = fields.String(validate=validate.OneOf(["read", "write", "admin"]))
    age = fields.Integer(allow_none=None, validate=validate.Range(min=16, max=25))


def check_schema_validator_validation():
    try:
        data = {
            "permission": "red",
            "age": 28
        }
        response = ApplySchemaValidator().load(data)
        pprint(response)
    except ValidationError as error:
        # Print Error Messages
        print("Print Errors: ")
        print(error.messages)

        print("\nValid datas :")
        # Get the valid data
        print(error.valid_data)


def is_even(data):
    if data % 2 != 0:
        raise ValidationError("Not an even value.")


class CustomValidator(Schema):
    data = fields.Float(validate=validate.And(validate.Range(min=4), is_even))


def check_custom_validator_validation():
    try:
        data = {
            "data": 3
        }
        response = CustomValidator().load(data)
        pprint(response)
    except ValidationError as error:
        # Print Error Messages
        print("Print Errors: ")
        print(error.messages)


class ValidateByMethod(Schema):
    data = fields.Float()

    @validates("data")
    def validate_quantity(self, value):
        if value < 0:
            raise ValidationError("Quantity must be greater than 0.")
        if value > 30:
            raise ValidationError("Quantity must not be greater than 30.")


def check_validate_by_method():
    try:
        data = {
            "data": 31
        }
        response = ValidateByMethod().load(data)
        pprint(response)
    except ValidationError as error:
        # Print Error Messages
        print("Print Errors: ")
        print(error.messages)


class SchemaValidation(Schema):
    password = fields.String()
    confirm_password = fields.String()

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data["password"] != data["confirm_password"]:
            raise ValidationError("Password not matched!", "confirm_password")


def check_schema_validation():
    try:
        data = {
            "password": "123",
            "confirm_password": "321"
        }
        response = SchemaValidation().load(data)
        pprint(response)
    except ValidationError as error:
        # Print Error Messages
        print("Print Errors: ")
        print(error.messages)


fields.Field.default_error_messages["required"] = "Empty value not allowed!"


class CustomErrorMessage(Schema):
    password = fields.String(required=True)


def check_custom_error_message():
    try:
        data = {}
        response = CustomErrorMessage().load(data)
        pprint(response)
    except ValidationError as error:
        # Print Error Messages
        print("Print Errors: ")
        print(error.messages)


if __name__ == '__main__':
    check_custom_validator_validation()
