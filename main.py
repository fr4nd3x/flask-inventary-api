from concurrent.futures import CancelledError
import email
from pyexpat import model
from sqlite3 import Date
from tracemalloc import start
from venv import create
from webbrowser import get
from zipapp import create_archive
from flask import Flask,jsonify, request  
import os 
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

#from app import routes
app=Flask(__name__)
if __name__ == "__main___":
    app.run(debug=True)

print (os.environ.get('SQLALCHEMY_DATABASE_URI'))
app.config['SQLALCHEMY_DATABASE_URI'] =os.environ.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)

class Movement(db.Model):
    __tablename__ = "move"
    id = db.Column(db.Integer(), primary_key=True)
    fullname= db.Column('fullName',db.String(50))
    email = db.Column(db.String(80))
    dependence_id= db.Column('dependence_id',db.String(50))
    dependence = db.Column(db.String(50 ))
    company = db.Column(db.Integer())
    reference = db.Column(db.String(50))
    date = db.Column(db.DateTime())
    dni = db.Column(db.Integer())
    create_date = db.Column(db.DateTime())
    Canceled = db.Column(db.Numeric(1))
    dalate_date = db.Column(db.DateTime(80))
    uid = db.Column(db.String(20))

    def _repr_(self):
        return f'< Movement {self.id}>'

class Move_detail (db.Model):
    #id = db.Column(db.Integer(), unique=True, nullable=False)
    id = db.Column(db.Integer(), primary_key=True)
    code_patrimonial= db.Column(db.Integer(), nullable=False)
    denomination= db.Column(db.String(30), unique=True, nullable=False)
    maraca = db.Column(db.String(10), unique=True, nullable=False)
    model = db.Column(db.String(20 ), unique=True, nullable=False)
    color = db.Column(db.String(10), unique=True, nullable=False)
    series = db.Column(db.String(20), unique=True, nullable=False)
    others= db.Column(db.String(20), unique=True, nullable=False)
    condition = db.Column(db.String(1), unique=True, nullable=False)
    observation = db.Column(db.String(50), unique=True, nullable=False)
    

    def _repr_(self):
        return f'< move_detail {self.id}>'

property_names=[p for p in dir(Movement) if isinstance(getattr(Movement,p),property)]
print( property_names)
db.create_all()
db.session.commit()

@app.route('/')
@app.route('/index')
def index():
    data={'id':1,'name':os.environ.get("MSG")}
    return jsonify(data)

@app.route('/in',methods=['POST'])
def in_post():
    o=request.json
    movement=Movement(  )
    db.session.add(movement)
    db.session.commit()
    return str( movement)  





@app.route('/in',methods=['POST'])
def in_post1():
    o=request.json
    move_detail = move_detail(email = o['email'])
    db.session.add(move_detail)
    db.session.commit()
    return str (move_detail.id)



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






