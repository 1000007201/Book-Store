from flask_restful import Resource
from flask import request, json, render_template, session
from .model import Users
from .validators import validate_register, validate_login, validate_change_pass
from .utils import get_otp, send_mail, get_token, token_short, token_required


class Registration(Resource):
    def post(self):
        """
            This api is for user registration to this application
            @return: Result Message after going through all validations
        """
        req_data = request.data
        body = json.loads(req_data)
        validate_data = validate_register(body)
        if validate_data:
            return validate_data
        try:
            del body['conf_password']
            user = Users(**body)
            user.save()
            otp = get_otp()
            token = get_token(otp, user.id)
            short_token = token_short(token)
            token_url = r"http://127.0.0.1:90/activate?token=" + f"{short_token}"
            template = render_template('index.html', data={'otp': otp, 'token_url': token_url})
            send_mail(template, body.get('email'))
            return {'Message': 'User Registered ', 'Code': 200}
        except Exception as e:
            return {'Error': str(e), 'Code': 500}


class Login(Resource):
    def post(self):
        """
        This API is used to authenticate user to access resources
        @param request: user credential like username and password
        @return: Returns success message and access token on successful login
        """
        req_data = request.data
        body = json.loads(req_data)
        validated_data = validate_login(body)
        try:
            if 'Error' in validated_data:
                return validated_data
            if 'Error-Active' in validated_data:
                otp = get_otp()
                token = get_token(otp, validated_data['user_id'])
                short_token = token_short(token)
                token_url = r"http://127.0.0.1:90/activate?token=" + f"{short_token}"
                template = render_template('index.html', data={'otp': otp, 'token_url': token_url})
                send_mail(template, validated_data.get('email'))
                return {'Message': 'Your account is not active yet check your registered Email', 'Code': 200}
            user_id = validated_data.get('user_id')
            if 'user_id' in session:
                if session['user_id'] == user_id:
                    return {'Message': 'You are already logged in', 'Code': 200}
            session.clear()
            session['logged_in'] = True
            session['user_id'] = user_id
            return {'Message': 'Logged in', 'Code': 200}
        except Exception as e:
            return {'Error': str(e), 'Code': 500}


class Activate(Resource):
    method_decorators = {'post': [token_required]}

    def post(self, otp, user_id):
        """
            This API accepts the changes the current password
            @param : current password and new password
            @return: success message and status code
        """
        req_data = request.data
        body = json.loads(req_data)
        otp1 = body.get('otp')
        try:
            if otp1 != otp:
                return {'Error': 'OTP is not valid', 'Code': 404}
            user = Users.objects.filter(id=user_id).first()
            user.update(is_active=True)
            return {'Message': 'You account is activated now you can login', 'Code': 200}
        except Exception as e:
            return {'Error': str(e), 'Code': 500}


class Logout(Resource):
    def get(self):
        """
        Clear the session
        :return: Message with status code
        """
        session.clear()
        return {'Message': 'Logged Out', 'Code': 200}


class ChangePassword(Resource):
    def patch(self):
        """
        Change the password of user
        :return: Message with status code
        """
        req_data = request.data
        body = json.loads(req_data)
        validate_data = validate_change_pass(body)
        if 'Error' in validate_data:
            return validate_data
        user = validate_data.get('user_instance')
        user.update(password=body.get('new_password'))
        return {'Message': 'Password Changed', 'Code': 200}


