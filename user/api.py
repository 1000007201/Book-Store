from flask_restful import Resource
from flask import request, json
from .model import Users
from .validators import validate_register


class Registration(Resource):
    def post(self):
        """
            This api is for user registration to this application
            @param request: user registration data like username, email, password
            @return: Result Message after going through all validations
        """
        req_data = request.data
        body = json.loads(req_data)
        validate_data = validate_register(body)
        if validate_data:
            return validate_data
        try:
            user = Users(**body)
            user.save()
            return {'Message': 'User Registered', 'Code': 200}
        except Exception as e:
            return {'Error': str(e), 'Code': 500}
