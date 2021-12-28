import datetime as dt
from pprint import pprint
from marshmallow import Schema, fields


class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()
        self.friends = []
        self.employer = None


class Blog:
    def __init__(self, title, author):
        self.title = title
        self.author = author


class BlogMultiAuthor:
    def __init__(self, title, authors):
        self.title = title
        self.author = authors


class BlogNesting:
    def __init__(self, title, related=[]):
        self.title = title
        self.related: list = related


class Product:
    def __init__(self, name, categories=[]):
        self.name = name
        self.categories: list = categories


class Category:
    def __init__(self, name, products=[]):
        self.name = name
        self.products: list = products


class ProductSchema(Schema):
    name = fields.String()
    categories = fields.List(fields.Nested(lambda: CategorySchema()))


class CategorySchema(Schema):
    name = fields.String()
    products = fields.List(fields.Nested(lambda: ProductSchema()))


class UserSchema(Schema):
    name = fields.String()
    email = fields.Email()
    created_at = fields.DateTime()


class BlogSchema(Schema):
    title = fields.String()
    author = fields.Nested(UserSchema)


class BlogMultiAuthorSchema(Schema):
    title = fields.String()
    author = fields.Nested(UserSchema, many=True)


class BlogNestingSchema(Schema):
    title = fields.String()
    related = fields.List(fields.Nested(lambda: BlogNestingSchema()))


def serialize_basic_nested_schema():
    user = User(name="HMTMCSE Education", email="hmtmcse.com@gmail.com")
    blog = Blog(title="Python Marshmallow Tutorial", author=user)
    result = BlogSchema().dump(blog)
    print(result)


def serialize_nested_schema_list():
    user = User(name="HMTMCSE Education", email="hmtmcse.com@gmail.com")
    touhid = User(name="Touhid", email="hmtmcse.com@gmail.com")
    blog = BlogMultiAuthor(title="Python Marshmallow Tutorial", authors=[user, touhid])
    result = BlogMultiAuthorSchema().dump(blog)
    pprint(result)


def serialize_self_nested_schema():
    related = [
        BlogNesting("Python Basic Coding"),
        BlogNesting("Python Flask Tutorial"),
    ]
    blog = BlogNesting(title="Python Marshmallow Tutorial", related=related)
    result = BlogNestingSchema().dump(blog)
    pprint(result)


def serialize_two_way_nested_schema():
    product_n = Product(name="Product N")
    category_1 = Category(name="Category 1", products=[product_n])
    category_2 = Category(name="Category 2", products=[product_n])
    product_1 = Product(name="Product 1", categories=[category_1, category_2])

    result = ProductSchema().dump(product_1)
    pprint(result)


if __name__ == '__main__':
    serialize_nested_schema_list()
