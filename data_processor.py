from pprint import pprint
from marshmallow import Schema, fields, pre_load, post_load, post_dump, pre_dump


class Blog:
    def __init__(self, title, author):
        self.title = title
        self.author = author


class BlogSchema(Schema):
    title = fields.String()
    author = fields.String()

    @post_load(pass_many=True)
    def post_load(self, data, many, **kwargs):
        print("Called post_load")
        return Blog(**data)

    @post_dump(pass_many=True)
    def post_dump(self, data, many, **kwargs):
        print("Called post_dump")
        return data

    @pre_load(pass_many=True)
    def pre_load(self, data, many, **kwargs):
        print("Called pre_load")
        return data

    @pre_dump(pass_many=True)
    def pre_dump(self, data, many, **kwargs):
        print("Called pre_dump")
        return data


if __name__ == '__main__':
    blog = Blog(title="Python Marshmallow Tutorial", author="HMTMCSE Education")
    blog_schema = BlogSchema()
    dict_object = blog_schema.dump(blog)
    print(dict_object)

    json_dict = {"title": "Python Marshmallow Tutorial", "author": "HMTMCSE Education"}
    blog_object = blog_schema.load(json_dict)
    pprint(blog_object)
