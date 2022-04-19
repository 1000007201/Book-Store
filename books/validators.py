from common.custom_validations import NullValue
from flask import session
from user.model import Users


def validate_add_book(body):
    try:
        for i in body:
            name = i.get('name')
            author = i.get('author')
            publisher = i.get('publisher')
            price = i.get('price')
            quantity = i.get('quantity')

            if not name and not author and not publisher and not price and not quantity:
                raise NullValue('You have to enter all values', 409)
    except NullValue as exception:
        return exception.__dict__