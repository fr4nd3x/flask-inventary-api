from turtle import register_shape
from xml.dom.expatbuilder import DOCUMENT_NODE
from flask_marshmallow import Marshmallow
from app import app,db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import  ForeignKey
from sqlalchemy import or_

# It's creating an instance of the Marshmallow class.
ma = Marshmallow(app)

def get_attrs(klass):
    # It returns a list of all the attributes of a class.
    # :param klass: The class you're trying to get the attributes from
    fields=[]
    # It's returning a list of all the attributes of a class.
    for k in dir(klass):
        try:
            att=getattr(klass, k)
            if not callable(att) and not k.startswith('_') and not k.endswith('_') and k not in [ "move",'date_format', 'datetime_format', 'decimal_format','serializable_keys', 'serialize_only', 'serialize_rules', '_sa_instance_state','serialize_types', 'time_format', 'metadata', 'query', 'query_class','registry']:
                fields.append(k)
        except:
            print("get_attrs: An exception occurred with "+k)
    return fields

# It's creating a class that inherits from the object class.
Base = declarative_base()

# Movement is a class that inherits from db.Model, SerializerMixin, Base
class Movement(db.Model, SerializerMixin,Base):
    __tablename__ = "move"
    id = db.Column(db.Integer(), primary_key=True)
    type =db.Column(db.String(1), nullable = False)
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
    adress= db.Column(db.String(20))
    reason= db.Column(db.String(50))
    document_authorization = db.Column(db.String(50))   
    register_code = db.Column(db.String(20))

    dni_destino= db.Column(db.Integer())
    fullName_destino= db.Column(db.String(50))
    email_destino = db.Column(db.String(50))
    proveedor_destino= db.Column(db.String(50))
    local_destino = db.Column(db.String(50))
    adress_destino= db.Column(db.String(20))


    _details = relationship("MoveDetail", back_populates="move")
    details= None

    # It's a decorator that is used to define a static method.
    @staticmethod
    def getList(offset,limit,args):
        # A function that returns a list of movements.
        # :param offset: 0
        # :param limit: 10
        # :param args: {'fullName': '', 'offset': '0', 'limit': '10'}
        offset=int(offset)
        limit=int(limit)
        fullName = args.get("fullName")
        query=Movement.query.filter(or_(Movement.canceled == 0 , Movement.canceled == None  ))
        # It's returning a list of movements.
        if fullName:
            fullName = "%{}%".format(fullName)
            query=query.filter(Movement.fullName.like(fullName))
        size= query.count()
        movements = query.offset(offset).limit(limit).all()
        result = movement_schema.dump(movements)
        return {
            'size':size,
            'data':result
        }
    def _repr_(self):
        return f'< Movement {self.id}>'

class User(db.Model, SerializerMixin,Base):
    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key=True)
    dni = db.Column(db.Integer())
    fullName= db.Column('fullName',db.String(50))
    email = db.Column(db.String(80))
    local = db.Column(db.String(80))
    adress= db.Column(db.String(80))

    @staticmethod
    def getList(offset,limit,args):
        # A function that returns a list of movements.
        # :param offset: 0
        # :param limit: 10
        # :param args: {'fullName': '', 'offset': '0', 'limit': '10'}
        offset=int(offset)
        limit=int(limit)
        fullName = args.get("fullName")
        query=User.query.filter(or_(User.canceled == 0 , User.canceled == None  ))
        # It's returning a list of movements.
        if fullName:
            fullName = "%{}%".format(fullName)
            query=query.filter(User.fullName.like(fullName))
        size= query.count()
        users = query.offset(offset).limit(limit).all()
        result = users_schema.dump(users)
        return {
            'size':size,
            'data':result
        }
    def _repr_(self):
        return f'< Movement {self.id}>'

# MoveDetail is a class that inherits from db.Model, SerializerMixin, and Base
class MoveDetail (db.Model, SerializerMixin,Base):
    __tablename__ = "move_detail"
    id = db.Column(db.Integer(), primary_key=True)
    moveId= db.Column('move_id',db.Integer(),ForeignKey("move.id"),nullable=False)
    codePatrimonial= db.Column('code_patrimonial',db.String(20))
    denomination= db.Column(db.String(30))
    marca = db.Column("marca",db.String(10))
    model = db.Column(db.String(20 ))
    color = db.Column(db.String(10))
    series = db.Column(db.String(20))
    others= db.Column(db.String(20))
    condition = db.Column(db.String(1))
    observation = db.Column(db.String(50))
    canceled = db.Column(db.Integer())
    numLote= db.Column("num_lote",db.String(50))
    dimention= db.Column(db.String(50))
    
    
    move = relationship("Movement",back_populates="_details")

    def _repr_(self):
        return {"id": self.id}

# It's creating the tables in the database.
with app.app_context():
    db.create_all()
    db.session.commit()

# It's setting the fields attribute of the Meta class to the result of the get_attrs function.
fields=get_attrs(Movement)
# The MoveSchema class inherits from the SQLAlchemyAutoSchema class, which is a class from the
# Marshmallow-SQLAlchemy package. The SQLAlchemyAutoSchema class is a subclass of the Marshmallow
# Schema class. The MoveSchema class is a subclass of the SQLAlchemyAutoSchema class
class MoveSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movement
        fields =get_attrs(Movement)

# It's setting the fields attribute of the Meta class to the result of the get_attrs function.
fields=get_attrs(MoveDetail)

# The MoveDetailSchema class inherits from the SQLAlchemyAutoSchema class, which is a class that
# inherits from the Schema class
class MoveDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MoveDetail
        fields =fields


fields=get_attrs(User)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = get_attrs(User)




# It's creating an instance of the MoveSchema class.
category_schema = MoveSchema()
movement_schema = MoveSchema(many=True)






