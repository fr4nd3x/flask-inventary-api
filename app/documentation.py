from distutils.command.upload import upload
from re import A
from shutil import move
from tokenize import String
from wsgiref.validate import WriteWrapper
from flask import Flask, request,Blueprint
from app.graphQL import graphql_server 
from flask_restx import Api
from app import app
from flask import  request, Blueprint, url_for
 

api = Api(app, version='1.0', title='INVENTARY-API', 
          description='Inventary API with flask and python.')

"""
@api.route('/in/<cadena:id>', endpoint='in')
@api.doc(params={"DNI":"dni",
                "Type":"type",
                "Full Name":"fullName",
                "Email":"email",
                "Dependense":"dependence",
                "Company":"company",
                "Reference":"reference",
                "Date":"date"})
class endIn(Resource):
    def get(self,id):
        return {}
        
    @api.response(403, 'Not Authorized')
    def post(self):
        api.abort(403)





@api.route('/token')
class tok(Resource):
    def postTok(self):
        pass

parser = reqparse.RequestParser()
parser.add_argument('Full Name ', type=str, help='variable 1')
parser.add_argument('Company ', type=str, help='variable 2')




@api.route('/graphQL')
class addData(Resource):
    def post(self):
        return graphql_server


@api.route('/moveID')
class MoveID(Resource):
    def get(self):
        return 

@api.route('/seed')
class add(Resource):
    def get(self):
        return 
        
@api.route('/url')
class url(Resource):
    def get(self):
        return

@api.route('/example')
class MyExample(Resource):
    def get(self):
       return ("This route not exist, only for test")







@api.route('/resource/')
class Resource1(Resource):
    @api.doc(security='apikey')
    def get(self):
        pass

    @api.doc(security='apikey')
    def post(self):
        pass
    




if __name__ == '__main__':
    app.run()"""