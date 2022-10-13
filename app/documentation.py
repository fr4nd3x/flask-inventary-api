from re import A
from tokenize import String
from wsgiref.validate import WriteWrapper
from flask import Flask, request,Blueprint 
from flask_restx import Api, Resource, reqparse
from app import app 
from app.routes import get_data,  move_get, seed, in_post, token_post
from app.graphQL import graphql_server
from flask import  request
import fields


api = Api(app, version='1.0', title='INVENTARY-API', 
          description='Inventary API with flask and python.')

app = Flask(__name__)

    
@api.route('/in/<id>', endpoint='in')
@api.doc(params={"DNI":"dni", 
                "Type":"type",
                "Full Name":"fullName",
                "Email":"email",
                "Dependense":"dependence",
                "Company":"company",
                "Reference":"reference",
                "Date":"date"})
class MyResource(Resource):
    def get(self, id):
        return {}

    @api.doc(responses={403: 'Not Authorized'})
    def post(self, id):
        api.abort(403)





@api.route('/token')
class tok(Resource):
    def postTok(self):

        return () 

parser = reqparse.RequestParser()
parser.add_argument('Full Name ', type=str, help='variable 1')
parser.add_argument('Company ', type=str, help='variable 2')

@api.route('/graphQL')
class addData(Resource):
    def post(self,id):
        args = parser.parse_args()
        post_var1 = args['fullName']
        post_var2 = args['company']
        return 'Hello : ' + post_var1 + post_var2 + id


@api.route('/ss')
class query(Resource):
    def get(self):
        
       return ("This route not exist, only for test")


@api.route('/moveID')
class MyResource(Resource):
    def get(self):
        return move_get



@api.route('/seed')
class add(Resource):
    def get(self):
        return seed
    

@api.route('/url')
class url(Resource):
    def get(self):
        
        return get_data


if __name__ == '__main__':
    app.run()
