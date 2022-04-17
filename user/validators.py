from .model import Users
from common.custom_validations import NullValue, AlreadyExist, InternalError, NotFound


def validate_register(body):
    user_name = body.get('user_name')
    email = body.get('email')
    name = body.get('name')
    phone_number = body.get('phone_number')
    PIN = body.get('PIN')
    address = body.get('address')
    password = body.get('password')
    password2 = body.get('conf_password')
    try:
        user = Users.objects(user_name=user_name)
        user_email = Users.objects(email=email)
        user_phone = Users.objects(phone_number=phone_number)

        if not user_name and not email and not name and not phone_number and not PIN and not address \
                and not password and not password2:
            raise NullValue('You have to enter all fields', 404)

        if password != password2:
            raise InternalError('Confirm your password correctly', 409)

        if user:
            raise AlreadyExist('User Name Already Exist', 409)

        if user_email:
            raise AlreadyExist('Email Already Exist', 409)

        if user_phone:
            raise AlreadyExist('Phone Number Already Exist', 409)
    except NullValue as exception:
        return exception.__dict__
    except AlreadyExist as exception:
        return exception.__dict__
    except InternalError as exception:
        return exception.__dict__


def validate_login(body):
    try:
        user_name = body.get('user_name')
        password = body.get('password')
        if not user_name and not password:
            raise NullValue('You have to enter all fields', 404)
        user = Users.objects.filter(user_name=user_name).first()
        if user.password != password:
            raise NotFound('Please Enter correct password!!', 404)
        if not user.is_active:
            return {'Error-Active': 'Your account is not active yet', 'Code': 409, 'user_id': user.id}
        return {'user_id': user.id}
    except NullValue as exception:
        return exception.__dict__
    except NotFound as exception:
        return exception.__dict__
