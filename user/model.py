from mongoengine import Document, SequenceField, StringField, EmailField, BooleanField


class Users(Document):
    id = SequenceField(primary_key=True)
    user_name = StringField(unique=True, required=True)
    name = StringField(max_length=50, required=True)
    email = EmailField(unique=True, required=True)
    phone_number = StringField(max_length=10, required=True)
    password = StringField(max_length=10, required=True)
    is_active = BooleanField(default=False)
    is_admin = BooleanField(default=False)
    PIN = StringField(max_length=6, required=True)
    address = StringField(max_length=250, required=True)
