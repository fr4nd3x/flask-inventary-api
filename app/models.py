from flask_marshmallow import Marshmallow
from app import app,db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import  ForeignKey
from sqlalchemy import or_

ma = Marshmallow(app)


def get_attrs(klass):
    
    # It returns a list of all the attributes of the class.
    # :param klass: The class you want to get the attributes of
    # It returns a list of all the attributes of the class.
    fields=[]
    for k in dir(klass):
        try:
            att=getattr(klass, k)
            if not callable(att) and not k.startswith('_') and not k.endswith('_') and k not in [ "move",'date_format', 'datetime_format', 'decimal_format','serializable_keys', 'serialize_only', 'serialize_rules', '_sa_instance_state','serialize_types', 'time_format', 'metadata', 'query', 'query_class','registry']:
                fields.append(k)
        except:
            print("get_attrs: An exception occurred with "+k)
    return fields
    return [k for k in dir(klass)
        if not callable(getattr(klass, k)) and not k.startswith('_') and not k.endswith('_') and k not in [ "move",'date_format', 'datetime_format', 'decimal_format','serializable_keys', 'serialize_only', 'serialize_rules', '_sa_instance_state','serialize_types', 'time_format', 'metadata', 'query', 'query_class','registry']]

Base = declarative_base()


# Movement is a class that inherits from db.Model, SerializerMixin, Base
class Movement(db.Model, SerializerMixin,Base):
    __tablename__ = "move"
    id = db.Column(db.Integer(), primary_key=True)
    type =db.Column(db.String(1))
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


    # A function that returns a list of movements.        
    # :param offset: 0
    # :param limit: 10
    # :param args: {'fullName': '', 'offset': 0, 'limit': 10}    
    @staticmethod
    def getList(offset,limit,args):
        """
        I'm trying to filter the query by the fullName parameter, but I'm getting an error
        
        :param offset: The offset of the first element to be returned
        :param limit: 10
        :param args: {'fullName': 'John'}
        :return: A list of dictionaries
        """


        offset=int(offset)
        limit=int(limit)
        fullName = args.get("fullName")
        query=Movement.query.filter(or_(Movement.canceled == 0 , Movement.canceled == None  ))

        # I'm trying to filter the query by the fullName parameter, but I'm getting an error.
        # :return: A list of dictionaries        
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
    
    move = relationship("Movement",back_populates="_details")
    def _repr_(self):
        return {"id": self.id}

with app.app_context():
    db.create_all()
    db.session.commit()

fields=get_attrs(Movement)


# It's a class that inherits from ma.SQLAlchemyAutoSchema and has a Meta class that has a model
# attribute that is set to Movement and a fields attribute that is set to the result of the get_attrs
# function
class MoveSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movement
        fields =get_attrs(Movement)

fields=get_attrs(MoveDetail)

# The MoveDetailSchema class inherits from the SQLAlchemyAutoSchema class, which is a class that
# inherits from the Schema class
class MoveDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MoveDetail
        fields =fields
        
category_schema = MoveSchema()
movement_schema = MoveSchema(many=True)

