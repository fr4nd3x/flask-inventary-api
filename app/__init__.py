from flask import Flask
import os 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
dburi  = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'inventory.db'))

app.config['SQLALCHEMY_DATABASE_URI'] =dburi
print(app.config['SQLALCHEMY_DATABASE_URI'])

db = SQLAlchemy(app)


from app import models,routes,auth_middleware





