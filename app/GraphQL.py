from flask_migrate import Migrate
from ariadne import gql, QueryType, make_executable_schema, graphql_sync
from app.models import Movement
from flask import request, jsonify,make_response
from ariadne.constants import PLAYGROUND_HTML
from app import app

# Define type definitions (schema) using SDL
type_defs = gql(
   
"""
   type Query {
         movements (offset:Int  limit: Int):[Movement]
    }
   type Movement {
       fullName: String
       dni: String
       type: String
       }  

   """
)

# Initialize query
query = QueryType()


# Endpoint 
# movements resolver (return movements )
@query.field('movements')
def movements(*_,offset=0,limit=50):
   
   
    return make_response(jsonify(Movement.getList(offset,limit,[movements.to_json() for movements in movements.query.all()])))


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
    

if __name__ == "__main__":   
   app.run(debug=True)
