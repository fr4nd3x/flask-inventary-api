from flask import request,Blueprint 
from flask_restx import Api, Resource,reqparse
from app import app 

api = Api(app,add_specs=False)

@api.route('/seed')
class HelloWorld(Resource):
    def get(self):
        return 'agrega registros '



parser = reqparse.RequestParser()

@api.route('/ids/<string:id>')
class Parameers(Resource):
    @api.doc(parser=parser)
    def post(self, id):
        return 'Delete :' + id





@api.route('/my-resource/')
class MyResource(Resource):
    @api.doc(id='get_something')
    def get(self):
        return {}


if __name__ == '__main__':
    app.run()