
from re import A
from shutil import move
from flask import Flask,jsonify, request  ,make_response
import os 
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from flask_marshmallow import Marshmallow
from sqlalchemy import  ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from collections.abc import Iterable



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
            if not callable(k) and not k.startswith('_') and not k.endswith('_') and k not in [ 'date_format', 'datetime_format', 'decimal_format','get_tzinfo','serializable_keys', 'serialize_only', 'serialize_rules', 'serialize_types', 'time_format', 'to_dict','metadata', 'query', 'query_class','registry']]

#--------------------------------------------------------------------------------------------------------------------
Base = declarative_base()

class Movement(db.Model, SerializerMixin,Base):
    __tablename__ = "move"
    id = db.Column(db.Integer(), primary_key=True)
    fullName= db.Column('fullName',db.String(50))
    email = db.Column(db.String(80))
    dependence_id= db.Column('dependence_id',db.String(50))
    dependence = db.Column(db.String(50 ))
    company = db.Column(db.Integer())
    reference = db.Column(db.String(50))
    date = db.Column(db.DateTime())
    dni = db.Column(db.Integer())
    createDate = db.Column(db.DateTime())
    Canceled = db.Column(db.Numeric(1))
    deleteDate = db.Column(db.DateTime(80))
    uid = db.Column(db.String(20))


    def _repr_(self):
        return f'< Movement {self.id}>'
#--------------------------------------------------------------------------------------------------------------------
class MoveDetail (db.Model, SerializerMixin,Base):
    __tablename__ = "move_detail"
    id = db.Column(db.Integer(), primary_key=True)
    moveId= db.Column('move_id',db.Integer(),ForeignKey("move.id"),nullable=False)
    code_patrimonial= db.Column(db.Integer())
    denomination= db.Column(db.String(30))
    marca = db.Column("marca",db.String(10))
    model = db.Column(db.String(20 ))
    color = db.Column(db.String(10))
    series = db.Column(db.String(20))
    others= db.Column(db.String(20))
    condition = db.Column(db.String(1))
    observation = db.Column(db.String(50))
    Move = relationship ("Movement", foreign_keys = [moveId])
    
   

    def _repr_(self):
        return f'< MoveDetail {self.id}>'
#--------------------------------------------------------------------------------------------------------------------


class MoveSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movement
        fields =get_attrs(Movement)




print(get_attrs(Movement))

category_schema = MoveSchema()
movement_schema = MoveSchema(many=True)   



db.create_all()
db.session.commit()

@app.route('/<offset>/<limit>')
@app.route('/index')
def index(offset=0,limit=50):
    offset=int(offset)
    limit=int(limit)
    fullName = request.args.get("fullName")
    query=Movement.query
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

def toJSON(o):
    schema = MoveSchema(many=isinstance(o, Iterable))
    return make_response(jsonify(schema.dump(o)))

@app.route('/<moveId>',methods=['GET'])
def move_get(moveId):
    moveId=int(moveId)
    movement = Movement.query.get(moveId)
    return toJSON(movement)

@app.route('/<moveId>/detail')
def moveDetail(moveId):
    page=int(page)
    size=int(size)
    code_patrimonial = request.args.get("code_patrimonial")
    offset=(page*size)
    limit=(size*(page+1))
    query=MoveDetail.query
    if code_patrimonial:
        code_patrimonial = "%{}%".format(code_patrimonial)
        query=query.filter(MoveDetail.code_patrimonial.like(code_patrimonial))
    size= query.count()
    moveDetails = query.offset(offset).limit(limit).all()
    result = movement_schema.dump(moveDetails)
    data = {
        'size':size,
        'data':result
    }
    return make_response(jsonify(data))

#--------------------------------------------------------------------------------------------------------------------------
@app.route('/seed',methods=['GET'])
def seed():
    for i in range(10):
        args={
            "fullName":"fullname-"+str(i),
            "email" :"email-" +str(i),

        }

        """""  
            dependence_id = 1,
            dependence = "dependence",
            company ="company" + i,
            reference = "reference" + i,
            dni= "dni" + i
            createDate =  date.today,
            uid = 1"""""
        
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
    return jsonify(str(True) )


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

#--------------------------------------------------------------------------------------------------------------------------






