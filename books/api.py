from flask_restful import Resource
from flask import request, json
from .model import Books
from .validators import validate_add_book
from middleware.auth import admin_required, login_required


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
