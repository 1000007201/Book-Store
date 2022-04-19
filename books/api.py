from flask_restful import Resource
from flask import request, json
from .model import Books
from .validators import validate_add_book
from middleware.auth import admin_required, login_required
from common.custom_validations import NotFound


class AddBooks(Resource):
    method_decorators = {'post': [admin_required, login_required]}

    def post(self):
        req_data = request.data
        body = json.loads(req_data)
        validated_data = validate_add_book(body)
        if validated_data:
            return validated_data
        for i in body:
            book = Books(**i)
            book.save()
        return {'Message': 'Books are added', 'Code': 200}


class ViewBooks(Resource):
    method_decorators = {'get': [login_required]}

    def get(self):
        list_ = []
        book = Books.objects
        for i in book:
            list_.append({'name': i.name,
                          'author': i.author,
                          'publisher': i.publisher,
                          'price': i.price,
                          'quantity': i.quantity})
        return {'data': list_, 'Code': 200}


class DeleteBook(Resource):
    method_decorators = {'delete': [admin_required]}

    def delete(self, book_id):
        try:
            book = Books.objects.filter(id=book_id).first()
            if not book:
                raise NotFound('Book not exist', 409)
            book.delete()
            return {'Message': 'Book Deleted', 'Code': 200}
        except NotFound as exception:
            return exception.__dict__
        except Exception as e:
            return {'Error': str(e), 'Code': 500}
