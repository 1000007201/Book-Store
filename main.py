import os
from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from db.utils import connect_db
from routes import all_routes
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
api = Api(app)
connect_db()


def connect_api():
    for i in all_routes:
        api_class = i[0]
        endpoint = i[1]
        api.add_resource(api_class, endpoint)


connect_api()

if __name__ == "__main__":
    app.run(debug=True, port=90, host="0.0.0.0")
