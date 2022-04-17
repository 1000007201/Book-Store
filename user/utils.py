import os
import random
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import jwt
from functools import wraps
import base64
from flask import request
import datetime
load_dotenv()


def get_otp():
    otp = random.randint(1000, 9999)
    return otp


def send_mail(bodyContent, email):
    EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')

    msg = MIMEMultipart()
    msg['Subject'] = 'Activate Account'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg.attach(MIMEText(bodyContent, "html"))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASS)
        smtp.send_message(msg)


def get_token(otp, user_id):
    token = jwt.encode({'otp': otp, 'user_id': user_id, 'Exp': str(datetime.datetime.utcnow() + datetime.timedelta(seconds=600))},
                       str(os.environ.get('SECRET_KEY')))
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'access-token' in request.headers:
            short_token = request.headers.get('access-token')
        else:
            short_token = request.args.get('token')
        token = true_token(short_token)
        if not token:
            return {'Message': 'Token is missing!', 'code': 409}
        try:
            data = jwt.decode(token, str(os.environ.get('SECRET_KEY')), algorithms=["HS256"])
        except Exception as e:
            return {'Error': str(e), 'code': 409}

        return f(data['otp'], data['user_id'])
    return decorated


def token_short(token):
    token_string_bytes = token.encode("ascii")

    base64_bytes = base64.b64encode(token_string_bytes)
    base64_string = base64_bytes.decode("ascii")

    return base64_string


def true_token(token_):
    base64_bytes = token_.encode("ascii")

    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")

    return sample_string
