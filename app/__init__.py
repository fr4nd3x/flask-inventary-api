from flask import Flask
import os 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import re

app = Flask(__name__)
cors = CORS(app)

print (os.environ.get('SQLALCHEMY_DATABASE_URI'))
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///inventory.db'
print (app.config['SQLALCHEMY_DATABASE_URI'] )

db = SQLAlchemy(app)

from app import models,routes,auth_middleware



