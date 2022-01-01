from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, ValidationError
from marshmallow_sqlalchemy import SQLAlchemySchema
from sqlalchemy.orm import session

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask-sqlalchemy.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer)
    income = db.Column(db.Float, default=0)


with app.app_context():
    db.create_all()


def is_empty(data):
    if not data or data == "":
        raise ValidationError("Empty value not allowed!")


class PersonSchema(SQLAlchemySchema):
    first_name = fields.String(required=True, validate=is_empty, error_messages={"required": "Please enter first name"})
    last_name = fields.String(allow_none=None)
    email = fields.Email(required=True, validate=is_empty, error_messages={"required": "Please enter email"})
    age = fields.Integer(allow_none=None)
    income = fields.Float(allow_none=None)

    class Meta:
        model = Person
        load_instance = True


@app.route('/')
def form():
    return '''
               <form action="/create" method="POST">
                   <div><label>First Name:</label><input type="text" name="first_name"></div>
                   <div><label>Last Name:</label><input type="text" name="last_name"></div>
                   <div><label>Email:</label><input type="email" name="email"></div>
                   <input type="submit" value="Submit">
               </form>
               '''


@app.route('/create', methods=["POST"])
def create():
    try:
        form_all_data = request.form
        person = PersonSchema().load(form_all_data, session=session)
        db.session.add(person)
        db.session.commit()
    except ValidationError as error:
        return error.messages
    response = "Data successfully Inserted"
    return response


@app.route('/list')
def list():
    response = ""
    persons = Person.query.all()
    if persons:
        response = PersonSchema().dumps(persons, many=True)
    return response


if __name__ == '__main__':
    app.run(debug=True)
