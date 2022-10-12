from functools import wraps
from flask import request
import os, traceback
import requests
import json

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            url = os.environ.get('OAUTH_URL')+'/api/me'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer %s' % token 

            }
            
            o = json.loads( requests.request("GET", url, headers=headers).content)

            
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
        except Exception as e:
            traceback.print_exc()
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated
    


