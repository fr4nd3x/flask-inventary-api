from functools import wraps
from flask import request
import os
import requests
import base64
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
                'Authorization': 'Basic %s' % token 
                #base64.b64encode('%s:%s' % (token,'sp')
            }
            print ("Bearer %s" % token)
            
            o = json.loads( requests.request("GET", url, headers=headers).content)

            if o["error"]:
                return o,401
            print (o) 
            current_user =  {"uid" :1, "name" : "franc"} 
            """if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
            if not current_user["active"]:
                abort(403)"""
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated
    


"""
import hashlib
import random
def generate_token(length=12):
#Genera un token único de 30 caracteres como máximo.
chars = list(
    'ABCDEFGHIJKLMNOPQRSTUVWYZabcdefghijklmnopqrstuvwyz01234567890'
)
random.shuffle(chars)
chars = ''.join(chars)
sha1 = hashlib.sha1(chars.encode('utf8'))
token = sha1.hexdigest()
return token[:length]

"""