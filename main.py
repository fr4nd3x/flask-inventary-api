from flask import Flask,jsonify  
import os 
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

#from app import routes



app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+mysqlconnector://'+USER+':'+PASS+'@'+HOST+'/'+DB
db = SQLAlchemy(app)

class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    bio = db.Column(db.Text)

    def _repr_(self):
        return f'<Student {self.firstname}>'



@app.route('/')
@app.route('/index')
def index():
    data={'id':1,'name':os.environ.get("MSG")}
    return jsonify(data)

@app.route('/in',methods=['POST'])
def in_post():
    return 1

@app.route('/out',methods=["POST"])
def out_post():
    return 1

@app.route('/detail',methods=["POST"])
def detail_post():
    return 1
    
@app.route('/movement',methods=["GET"])
def movement_get():
    data={'id':1,'name':'mary'}
    return jsonify(data)
