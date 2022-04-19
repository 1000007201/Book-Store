from mongoengine import Document, SequenceField, StringField, IntField


class Books(Document):
    id = SequenceField(primary_key=True)
    name = StringField(max_length=50, required=True)
    author = StringField(max_length=50, required=True)
    publisher = StringField(max_length=50, required=True)
    price = IntField(required=True)
    quantity = IntField(required=True)
