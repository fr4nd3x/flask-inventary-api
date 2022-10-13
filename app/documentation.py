from re import A
from wsgiref.validate import WriteWrapper
from flask import request,Blueprint 
from flask_restx import Api, Resource,reqparse
from app import app 
from app.routes import get_data,  move_get, seed, in_post, token_post
from app.graphQL import graphql_server
from flask import  request



api = Api(app, version='2.0', title='INVENTARY-API', 
          description='Inventary API with flask and python.')





parser = reqparse.RequestParser()
parser.add_argument('PageSize', type=int, location='args')
parser.add_argument('Full Name ', type=str, help='variable 1')
parser.add_argument('Company ', type=str, help='variable 2')

@api.route('/in')
class  addIn(Resource):
    def post(self,id):
        args = parser.parse_args()
        var1 = args['fullName']
        var2 = args['company']
        return (in_post) +var1 +var2 

@api.route('/token')
class  tok(Resource):
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
