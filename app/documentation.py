from flask import request,Blueprint 
from flask_restx import Api, Resource,reqparse
from app import app 
from app.routes import get_data,  move_get, seed
from app.graphQL import graphql_server
from flask import  request, Flask
from app.models import db,relationship


api = Api(app, version='2.0', title='INVENTARY-API', 
          description='Inventary API with flask and python.')







parser = reqparse.RequestParser()
parser.add_argument('Full Name ', type=str, help='variable 1')
parser.add_argument('Company ', type=str, help='variable 2')

@api.route('/in')
class addData(Resource):
    def post(self,id):
        args = parser.parse_args()
        post_var1 = args['fullName']
        post_var2 = args['company']
        return 'Hello : ' + post_var1 + post_var2 + id

@api.route('/seed')
class add(Resource):
    def get(self):
        return seed

@api.route('/url')
class url(Resource):
    def get(self):
        return get_data
        

@api.route('/graphql')
class query(Resource):
    def get(self):
        return graphql_server


@api.route('/moveID')
class MyResource(Resource):
    def get(self):
        return move_get


"""
parser = reqparse.RequestParser()
parser.add_argument('Full Name ', type=str, help='')
parser.add_argument('Company', type=str, help='')
@api.route('/in/<string:id>')
class HelloWorldParameter(Resource):
    @api.doc(parser=parser)
    def post(self,id):
        args = parser.parse_args()
        post_var1 = args['']
        post_var2 = args['']
        return 'Hello : ' + post_var1 + post_var2 + id
"""


"""

class Movement(db.Model):
    '''
        description: User description
    '''
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
    @jsonapi_rpc(http_methods=['POST''GET'])
    def send_mail(self, email):
        '''
            description : Send an email
            args:
                email:
                    type : string 
                    example : test email
        '''
        content = 'Mail to {} : {}\n'.format(self.name, email)
        return { 'result' : 'sent {}'.format(content)}

"""



if __name__ == '__main__':
    app.run()
