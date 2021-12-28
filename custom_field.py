from pprint import pprint
from marshmallow import fields, ValidationError, Schema


class PinCode(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return "".join(str(d) for d in value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return [int(c) for c in value]
        except ValueError as error:
            raise ValidationError("Pin codes must contain only digits.") from error


class UserSchema(Schema):
    name = fields.String()
    email = fields.String()
    pin_code = PinCode()


if __name__ == '__main__':
    try:
        data = {
            "name": "HMTMCSE Education",
            "email": "hmtmcse.com@gmail.com",
            "pin_code": "123x",
        }
        response = UserSchema().load(data)
        pprint(response)
    except ValidationError as error:
        # Print Error Messages
        print("Print Errors: ")
        print(error.messages)
