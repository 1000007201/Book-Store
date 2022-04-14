from .model import Users
from common.custom_validations import NullValue, AlreadyExist


def validate_register(body):
    user_name = body.get('user_name')
    email = body.get('email')
    name = body.get('name')
    phone_number = body.get('phone_number')
    PIN = body.get('PIN')
    address = body.get('address')
    try:
        user = Users.objects(user_name=user_name)
        user_email = Users.objects(email=email)
        user_phone = Users.objects(phone_number=phone_number)

        if not user_name and not email and not name and not phone_number and not PIN and not address:
            raise NullValue('You have to enter all fields', 404)

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

