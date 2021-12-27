from marshmallow import Schema, fields


class AllFieldSchema(Schema):
    isActive = fields.Boolean(required=True, error_messages={"required": "Please check active."})
    name = fields.String(required=True, error_messages={"required": "Please enter name."})
    email = fields.Email()
    age = fields.Integer(required=True, error_messages={"required": "Please enter age."})
    salary = fields.Decimal()
    houseRent = fields.Float()
    foodCost = fields.Number()
    dateOfBirth = fields.Date()
    officeTime = fields.Time()
    checkIn = fields.DateTime()
    otherDetails = fields.Dict(keys=fields.String(), values=fields.String(), required=False)
    certificates = fields.List(fields.String)
    identity = fields.Function(lambda data: data.name + "something")
    isUnder18 = fields.Method("is_under_18")
    lastAccess = fields.IP()
    webAddress = fields.URL()
    uuid = fields.UUID()

    def is_under_18(self, data):
        if data.age < 18:
            return True
        return False

