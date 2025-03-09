from flask import Flask,request,render_template
from flask_restful import Api
import database
from flask_jwt_extended import JWTManager,jwt_required,get_jwt_identity
from datetime import timedelta

from modules.api import routes
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URI']
app.config["JWT_SECRET_KEY"] = os.environ['JWT_SECRET_KEY']
app.config["JWT_VERIFY_SUB"]=False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

@app.route('/')
def auth_page():
    return render_template('auth.html')

@app.route('/wikipedia')
def wikipedia_page():
    return render_template('wikipedia.html')

database.init_db(app)

jwt = JWTManager(app)

api = Api(app)

routes.init_routes(api)

# with app.app_context():
#     from database import db
#     db.create_all()
