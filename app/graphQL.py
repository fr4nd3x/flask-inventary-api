from app import app
from flask_migrate import Migrate
from ariadne import gql, QueryType, make_executable_schema, graphql_sync
from app.models import Movement,get_attrs,fields
from flask import request, jsonify
from ariadne.constants import PLAYGROUND_HTML
from app.auth_middleware import token_required
# Define type definitions (schema) using SDL

fields=get_attrs(Movement)

f = """

      fullName: String
      dni: String
      type: String
"""
f=""
for f0 in fields:
   f+=(f0+":String ")
print(f)

type_defs = gql(
   
"""
   type Query {
      movements (offset:Int  limit: Int):Result
   }
   type Result{
      data:[Movement]!
      size:Int
   }
   type Movement {
"""
+f+
"""
   }  

   """
)

# Initialize query
query = QueryType()

# Endpoint 
# movements resolver (return movements )
@query.field('movements')
@token_required
def movements(*_,offset=0,limit=50):   
   print(request.args)
   return Movement.getList(offset,limit,request.args)

#@query.field("movements") 
# def movements(*_):moveDetailSchema(details)
#return Movement.getList()
#return 
#return Movement.getList(offset,limit,{})

schema = make_executable_schema(type_defs,query)



# initialize flask app
@app.route("/graphql", methods=["GET"])
def graphql_playground():
   # Playground accepts GET requests only.
   # If you wanted to support POST you'd have to
   # change the method to POST and set the content
   # type header to application/graphql

   return PLAYGROUND_HTML
# Create a GraphQL endpoint for executing GraphQL queries

@app.route("/graphql", methods=["POST"])
def graphql_server():

   data = request.get_json()
   success, result = graphql_sync(schema, data, context_value = {"request": request})
   status_code = 200 if success else 400
   return jsonify(result), status_code
   
