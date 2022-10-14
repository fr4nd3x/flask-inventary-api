from flask import Flask
import os 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import restx_monkey as monkey

monkey.patch_restx()

# Creating a Flask app and enabling CORS.
app = Flask(__name__)
cors = CORS(app)

# Setting the database URI.
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI  = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'inventory.db'))
app.config['SQLALCHEMY_DATABASE_URI'] =SQLALCHEMY_DATABASE_URI
print(SQLALCHEMY_DATABASE_URI)

# Creating a database object.
db = SQLAlchemy(app)

# Importing the modules from the app folder.
from app import graphQL, models,routes,auth_middleware,documentation





