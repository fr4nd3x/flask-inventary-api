from functools import wraps
from flask import request
import os, traceback
import requests
import json
# A decorator function. It is a function that takes another function as an argument, adds some kind of
# functionality and returns another function. In this case, it takes a function as an argument and
# returns a new function that wraps the original function and adds the functionality of checking for a
# valid JWT token.
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):# A decorate function
        if os.environ.get('TEST',0)==1:
            return f({'uid':1,'name':'test'}, *args, **kwargs)
        token = None
         # Checking if the request has an Authorization header. If it does, it splits the value of the header.
         # by a space and takes the second part.
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        # Checking if the request has an Authorization header. If it does, it splits the value of the
        # header
        # by a space and takes the second part.
        if not token:
            print(request.full_path)
            print(request.endpoint)
            # This is a hack to get around the fact that the GraphQL server does not have a way to
            # return a 401 error.
            if request.endpoint == "graphql_server":
                raise Exception("Unauthorized")
            return {
                "message": "Authentication Token is missing!",
                "error": "Unauthorized",
                "data":[]
            }, 401
        # Calling the OAuth server to validate the token.
        try:
            url = os.environ.get('OAUTH_URL')+'/api/me'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer %s' % token 

            }
            
            # Calling the OAuth server to validate the token.
            o = json.loads( requests.request("GET", url, headers=headers).content)

            # Checking if the token is valid or not.
            if "error" in o:
                return o,401
            current_user =  {"uid" :o["id"], "name" : o['name']} 
            """if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
            if not current_user["active"]:
                abort(403)"""
        # This is a catch-all exception handler. It catches any exception that is thrown in the try
        # block and
        # returns a 500 error.
        except Exception as e:
            traceback.print_exc()
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        # Calling the function that was passed to the decorator function.
        return f(current_user, *args, **kwargs)

    return decorated
    


