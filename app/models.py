from flask_marshmallow import Marshmallow
from app import app,db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import  ForeignKey

ma = Marshmallow(app)

def get_attrs(klass):
  return [k for k in dir(klass)
            if not callable(k) and not k.startswith('_') and not k.endswith('_') and k not in [ "move",'date_format', 'datetime_format', 'decimal_format','get_tzinfo','serializable_keys', 'serialize_only', 'serialize_rules', '_sa_instance_state','serialize_types', 'time_format', 'to_dict','metadata', 'query', 'query_class','registry']]

Base = declarative_base()

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

    def _repr_(self):
        return f'< Movement {self.id}>'
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

fields=get_attrs(Movement)


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