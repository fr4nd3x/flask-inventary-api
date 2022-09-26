
from email import message
from re import A
from shutil import move
from wsgiref.util import application_uri
from flask import Flask,jsonify, request  ,make_response, Response
import os 
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from flask_marshmallow import Marshmallow
from sqlalchemy import  ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.declarative import declarative_base
from flask_graphql import GraphQLView
from sqlalchemy import or_, not_, and_
from collections.abc import Iterable
import requests
import tempfile
from app.auth_middleware import token_required
app=Flask(__name__)
ma = Marshmallow(app)
cors = CORS(app)
if __name__ == "__main___":
    app.run(debug=True)

print (os.environ.get('SQLALCHEMY_DATABASE_URI'))
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///inventory.db'
print (app.config['SQLALCHEMY_DATABASE_URI'] )
#--------------------------------------------------------------------------------------------------------------------
db = SQLAlchemy(app)
def get_attrs(klass):
  return [k for k in dir(klass)
            if not callable(k) and not k.startswith('_') and not k.endswith('_') and k not in [ "move",'date_format', 'datetime_format', 'decimal_format','get_tzinfo','serializable_keys', 'serialize_only', 'serialize_rules', '_sa_instance_state','serialize_types', 'time_format', 'to_dict','metadata', 'query', 'query_class','registry']]

#--------------------------------------------------------------------------------------------------------------------
Base = declarative_base()

class Movement(db.Model, SerializerMixin,Base):
    __tablename__ = "move"
    id = db.Column(db.Integer(), primary_key=True)
    fullName= db.Column('fullName',db.String(50))
    email = db.Column(db.String(80))
    dependence_id= db.Column('dependence_id',db.String(50))
    dependence = db.Column(db.String(50 ))
    company = db.Column(db.String(50))
    reference = db.Column(db.String(50))
    date = db.Column(db.DateTime())
    dni = db.Column(db.Integer())
    createDate = db.Column(db.DateTime())
    canceled = db.Column(db.Integer())
    deleteDate = db.Column(db.DateTime())
    uid = db.Column(db.String(20))

    _details = relationship("MoveDetail", back_populates="move")
    details= None

    def _repr_(self):
        return f'< Movement {self.id}>'
#--------------------------------------------------------------------------------------------------------------------
class MoveDetail (db.Model, SerializerMixin,Base):
    __tablename__ = "move_detail"
    id = db.Column(db.Integer(), primary_key=True)
    moveId= db.Column('move_id',db.Integer(),ForeignKey("move.id"),nullable=False)
    codePatrimonial= db.Column('code_patrimonial',db.Integer())
    denomination= db.Column(db.String(30))
    marca = db.Column("marca",db.String(10))
    model = db.Column(db.String(20 ))
    color = db.Column(db.String(10))
    series = db.Column(db.String(20))
    others= db.Column(db.String(20))
    condition = db.Column(db.String(1))
    observation = db.Column(db.String(50))
    canceled = db.Column(db.Integer())
    
    move = relationship("Movement",back_populates="_details")
   

    def _repr_(self):
        return {"id": self.id}
#--------------------------------------------------------------------------------------------------------------------

fields=get_attrs(Movement)
print(fields)

class MoveSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movement
        fields =get_attrs(Movement)

fields=get_attrs(MoveDetail)
print(fields)
class MoveDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MoveDetail
        fields =fields
        
category_schema = MoveSchema()
movement_schema = MoveSchema(many=True)   



db.create_all()
db.session.commit()

@app.route('/<offset>/<limit>')
@app.route('/index')
@token_required
def index(user,offset=0,limit=50):
    print(user)
    offset=int(offset)
    limit=int(limit)
    fullName = request.args.get("fullName")
    query=Movement.query.filter(or_(Movement.canceled == 0 , Movement.canceled == None  ))


    if fullName:
        fullName = "%{}%".format(fullName)
        query=query.filter(Movement.fullName.like(fullName))
    size= query.count()
    movements = query.offset(offset).limit(limit).all()
    result = movement_schema.dump(movements)
    data = {
        'size':size,
        'data':result
    }
    return make_response(jsonify(data))

def _json(o):
    response = make_response(
        jsonify(o)
    )
    response.headers["Content-Type"] = "application/json"
    return response


#

@app.route('/<idd>',methods=['PUT'])
@token_required
def move_put(user,ids):


    for moveId in ids.split(','):
        moveId=int(moveId)
        movement = Movement.query.get(moveId)
        movement.add=1
        db.session.merge(movement)

    db.session.commit()
    return _json(1)

#


@app.route('/<ids>',methods=['DELETE'])

def move_delete(ids):


    for moveId in ids.split(','):
        moveId=int(moveId)
        movement = Movement.query.get(moveId)
        movement.canceled=1
        db.session.merge(movement)
    
    if id ():
        message.filter_by(fullname=id) 
        db.session = request.args.get(db.session)
    if db.session():
        message.filter_by(db.session)
    if move_detail ():
        message.filter_by(move_detasil= move_detail)

    db.session.delete(move_detail)
    db.session.commit()
    return _json(1)


@app.route('/<moveId>/detail')
def move_detail(moveId):
    page=int(page)
    size=int(size)
    codePatrimonial = request.args.get("codePatrimonial")
    offset=(page*size)
    limit=(size*(page+1))
    query=MoveDetail.query
    if codePatrimonial:
        codePatrimonial = "%{}%".format(codePatrimonial)
        query=query.filter(MoveDetail.codePatrimonial.like(codePatrimonial))
    size= query.count()
    moveDetails = query.offset(offset).limit(limit).all()
    result = movement_schema.dump(moveDetails)
    data = {
        'size':size,
        'data':result
    }
    return _json(data)

#--------------------------------------------------------------------------------------------------------------------------
@app.route('/seed',methods=['GET'])
def seed():
    for i in range(10):
        args={
            "fullName":"fullname-"+str(i),
            "email" :"email-" +str(i),
        }

        
        movement=Movement(**args)
        db.session.add(movement)
        db.session.commit()
        for j in range(10):
            args={
                "moveId" :movement.id
            }
            movementDet=MoveDetail(**args)
            db.session.add(movementDet)  
    db.session.commit()
    return jsonify(str(True))


@app.route('/token',methods=['POST'])
def token_post():
    o=request.json
    try:    
        token=o['code']
        
        return str( token) 
    except Exception as e:
        return jsonify(str(e) )

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
     
@app.route('/detail',methods=["POST"])
def detail_post():
    o=request.json
    try:    
        values = {}
        for y in get_attrs(MoveDetail):
            try:
                values[y]=o[y]
            except KeyError:
                print("Variable "+y+" is empty")
        moveDetail=MoveDetail(**values)
        db.session.add(moveDetail)
        db.session.commit()
        
        return str( moveDetail) 
    except Exception as e:
        return jsonify(str(e))


@app.route('/url',)
def get_data():
    #SaveToFile(move_get(5).get_data(as_text=True).'data.json')
    temp = tempfile.TemporaryFile()
    """with open () as f :
        f.write (stuff)""" 
    m=_move_get(5)
    m=[m]
    temp.write(jsonify(m).get_data(as_text=False))
    temp.seek(0)
    data=temp.read()
    temp.close()
    conten =  requests.post('http://web.regionancash.gob.pe/api/jreport/', 
        files={'file':data },
        data={'filename': 'data.json','template':'pad'}).content
   
    return Response(conten, mimetype='application/pdf')


def _move_get(moveId):
    try:
        int(moveId)
    except Exception as e:
        print(e)
        return None
    moveId=int(moveId)
    movement = Movement.query.get(moveId)
    details=movement._details
    db.session.expunge(movement)
    for detail in details:
        db.session.expunge(detail)
    movementSchema = MoveSchema()   
    movement=movementSchema.dump(movement)
    moveDetailSchema = MoveDetailSchema(many=True) 
    movement['details']=moveDetailSchema.dump(details)
    return movement

@app.route('/<moveId>')
def move_get(moveId):
    return jsonify(_move_get(moveId))
    

