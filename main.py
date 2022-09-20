from concurrent.futures import CancelledError
import email
from pyexpat import model
from sqlite3 import Date
from tracemalloc import start
from venv import create
from webbrowser import get
from zipapp import create_archive
from flask import Flask,jsonify, request  ,make_response
import os 
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from flask_marshmallow import Marshmallow



from sqlalchemy.orm import class_mapper

#from app import routes
app=Flask(__name__)
ma = Marshmallow(app)
cors = CORS(app)
if __name__ == "__main___":
    app.run(debug=True)

print (os.environ.get('SQLALCHEMY_DATABASE_URI'))
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///inventory.db'
print (app.config['SQLALCHEMY_DATABASE_URI'] )
#os.environ.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
def get_attrs(klass):
  return [k for k in dir(klass)
            if not k.startswith('_') and not k.endswith('_') and k not in ['metadata', 'query', 'query_class','registry']]


class Movement(db.Model, SerializerMixin):
    __tablename__ = "move"
    id = db.Column(db.Integer(), primary_key=True, unique=True)
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
##print(dir(Movement))
#property_names=[p for p in dir(Movement) if isinstance(getattr(Movement,p),property)]
#print( property_names)
#for name in Movement().property_names():
#    print(name)

class MoveDetail (db.Model, SerializerMixin):
    #id = db.Column(db.Integer(), unique=True, nullable=False)
    __tablename__ = "Move_detail"
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    code_patrimonial= db.Column(db.Integer(), nullable=False)
    denomination= db.Column(db.String(30), unique=True, nullable=False)
    marca = db.Column(db.String(10), unique=True, nullable=False)
    model = db.Column(db.String(20 ), unique=True, nullable=False)
    color = db.Column(db.String(10), unique=True, nullable=False)
    series = db.Column(db.String(20), unique=True, nullable=False)
    others= db.Column(db.String(20), unique=True, nullable=False)
    condition = db.Column(db.String(1), unique=True, nullable=False)
    observation = db.Column(db.String(50), unique=True, nullable=False)


    def _repr_(self):
        return f'< move_detail {self.id}>'

    def __str__(self) -> str:



        return super().__str__()
#print(type(Movement.__table__))

#for x in Movement.__table__.columns:        
#    print(type(x))
#for x in Movement.__table__.columns._data.keys():
#    print(x)


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movement
        fields = ('id', 'name', 'short_desc') # fields to expose

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


db.create_all()
db.session.commit()



@app.route('/')
@app.route('/index')
def index():

#request.
    all_categories = Movement.query.all()
    result = categories_schema.dump(all_categories)

    data = {
        'message': 'All Categories!',
        'status': 200,
        'data': result
    }
    return make_response(jsonify(data))


@app.route('/in',methods=['POST'])
def in_post():
    o=request.json
    try:    
        values = {}
        for x in get_attrs(Movement):
            try:
                values[x]=o[x]
                if x=='date':
                    values[x]=datetime.strptime(values[x], '%Y-%m-%d %H:%M:%S')
            except KeyError:
                print("Variable "+x+" is empty")
        movement=Movement(**values)
    
        db.session.add(movement)
        db.session.commit()
        
        return str( movement) 
    except Exception as e:
        return jsonify(str(e) )
     





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
    data= [{'id': 1,
'order_num': 'N° 0118-2022-SGCP', 
'fullname_user': 'Abog. EVELIN MARGOT CUIZANO COLONIA',
'unidad_organica': 'SUB - GERENCIA DE RECURSOS HUMANOS - AREA BIENESTAR SOCIAL',
'local': 'SEDE CENTRAL DEL GOBIERNO REGIONAL DE ANCASH',
'date': '11/03/2022'},
{'id': 2,
'order_num': 'N° 0119-2022-SGCP' ,
'fullname_user': 'Abog. EVELIN MARGOT CUIZANO COLONIA',
'unidad_organica': 'SUB - GERENCIA DE RECURSOS HUMANOS - AREA BIENESTAR SOCIAL',
'local': 'SEDE CENTRAL DEL GOBIERNO REGIONAL DE ANCASH',
'date': '11/03/2022'},
{
'id': 3,
'order_num': 'N° 0120-2022-SGCP' ,
'fullname_user': 'Abog. EVELIN MARGOT CUIZANO COLONIA',
'unidad_organica': 'SUB - GERENCIA DE RECURSOS HUMANOS - AREA BIENESTAR SOCIAL',
'local': 'SEDE CENTRAL DEL GOBIERNO REGIONAL DE ANCASH',
'date': '11/03/2022'
},
{'id': 4,
'order_num': 'N° 0121-2022-SGCP' ,
'fullname_user': 'Abog. EVELIN MARGOT CUIZANO COLONIA',
'unidad_organica': 'SUB - GERENCIA DE RECURSOS HUMANOS - AREA BIENESTAR SOCIAL',
'local': 'SEDE CENTRAL DEL GOBIERNO REGIONAL DE ANCASH',
'date': '11/03/2022'
}



    ]
    return jsonify(data)    






