
from flask_migrate import Migrate
from ariadne import gql, QueryType, make_executable_schema, graphql_sync
from app.GraphQL import type_defs, query
from ariadne.constants import PLAYGROUND_HTML

# Define type definitions (schema) using SDL
type_defs = gql(
   """
   type Query {
       movements: [Movement]
   }


   type Movement {
       fullname: String!
       dni: String!
       type: String!
       }  

   """
)

# Initialize query

query = QueryType()


# places resolver (return places )
@query.field("movements")
def movements(*_):
   return [place.to_json() for place in Movement.query.all()]


schema = make_executable_schema(type_defs, [query])

# initialize flask app


# Create a GraphQL Playground UI for the GraphQL schema



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
   success, result = graphql_sync(schema, data, context_value={"request": request})
   status_code = 200 if success else 400
   return jsonify(result), status_code
    




