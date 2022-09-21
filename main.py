
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
#--------------------------------------------------------------------------------------------------------------------
db = SQLAlchemy(app)
def get_attrs(klass):
  return [k for k in dir(klass)
            if not callable(k) and not k.startswith('_') and not k.endswith('_') and k not in [ 'date_format', 'datetime_format', 'decimal_format','get_tzinfo','serializable_keys', 'serialize_only', 'serialize_rules', 'serialize_types', 'time_format', 'to_dict','metadata', 'query', 'query_class','registry']]

#--------------------------------------------------------------------------------------------------------------------
class Movement(db.Model, SerializerMixin):
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
    create_date = db.Column(db.DateTime())
    Canceled = db.Column(db.Numeric(1))
    dalate_date = db.Column(db.DateTime(80))
    uid = db.Column(db.String(20))

    def _repr_(self):
        return f'< Movement {self.id}>'
#--------------------------------------------------------------------------------------------------------------------
class MoveDetail (db.Model, SerializerMixin):
    __tablename__ = "Move_detail"
    id = db.Column(db.Integer(), primary_key=True)
    moveId= db.Column("move_id",db.Integer(),nullable=False)
    code_patrimonial= db.Column(db.Integer())
    denomination= db.Column(db.String(30))
    marca = db.Column("marca",db.String(10))
    model = db.Column(db.String(20 ))
    color = db.Column(db.String(10))
    series = db.Column(db.String(20))
    others= db.Column(db.String(20))
    condition = db.Column(db.String(1))
    observation = db.Column(db.String(50)) 
    def _repr_(self):
        return f'< MoveDetail {self.id}>'
#--------------------------------------------------------------------------------------------------------------------

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movement
        fields =get_attrs(Movement)
    class meta:
        model = MoveDetail
        fields =get_attrs(MoveDetail) # fields to expose


print(get_attrs(MoveDetail))
print(get_attrs(Movement))

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)   



db.create_all()
db.session.commit()

@app.route('/')
@app.route('/index')
def index():

    code_patrimonial = request.args.get("code_patrimonial")
    page = 0
    offset=(page*50)
    limit=(50*page+1)
    query=MoveDetail.query
    if code_patrimonial:
        code_patrimonial = "%{}%".format(code_patrimonial)
        query=query.filter(MoveDetail.code_patrimonial.like(code_patrimonial))
    size= query.count()
    moveDetails = query.offset(offset).limit(limit).all()
    result = categories_schema.dump(moveDetails)
    data = {

        'size':size,
        'data':result
    }

#-------------------------------------------------------------------------------------------
    fullName = request.args.get("fullName")
    page=0
    offset=(page*50)
    limit=(50*page+1)
    query=Movement.query
    if fullName:
        fullName = "%{}%".format(fullName)
        query=query.filter(Movement.fullName.like(fullName))
    size= query.count()
    movements = query.offset(offset).limit(limit).all()
    result = categories_schema.dump(movements)
    data = {
        'size':size,
        'data':result
    }

    return make_response(jsonify(data))

#--------------------------------------------------------------------------------------------------------------------------

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






