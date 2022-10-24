from xml.dom.minidom import Document
from app import app,db
from flask import request, jsonify,json
from app.auth_middleware import token_required
from app.models import get_attrs,Movement,movement_schema,MoveDetail,MoveDetailSchema,MoveSchema
from datetime import datetime
from email import message
from flask import  request ,make_response, Response,send_from_directory,jsonify
from sqlalchemy import or_
import tempfile
import os 
import requests
import base64
import random,string

# It takes a user object and an offset and limit, and returns a json response with the data  
# :param o: The object to be serialized
# :return: A response object.
@app.route('/<offset>/<limit>')
@app.route('/index')
@token_required
def index(user,offset=0,limit=50):
    print(user)
    offset=int(offset)
    limit=int(limit)
    fullName = request.args.get("fullName")
    type = request.args.get("type")
    query=Movement.query.filter(or_(Movement.canceled == 0 , Movement.canceled == None  ))
    if fullName and dni :
        fullName = "%{}%".format(fullName)
        dni = "%{}%".format(dni)
        query=query.filter(Movement.fullName.like(fullName))
        query=query.filter(Movement.dni.like(dni))
    if type:
        type = "%{}%".format(type)
        query=query.filter(Movement.type.like(type))
    size= query.count()
    movements = query.offset(offset).limit(limit).all()
    result = movement_schema.dump(movements)
    data = {
        'size':size,
        'data':result
    }
    return make_response(jsonify(data))
def _json(o):
    response = make_response(
        jsonify(o)
    )
    response.headers["Content-Type"] = "application/json"
    return response


# It creates 10 movements and for each movement it creates 10 movement details
# :param user: The user object that is returned by the token_required decorator
# :return: A list of Movement objects.
def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

@app.route('/seed',methods=['GET'])
@token_required
def seed(user):
    marks = ['Lenovo', 'hp', 'asus', 'mac']
    conditions = ['R', 'M', 'B']
    peoples = []
    for i in range(5):
        peoples.append({
            "dni":''.join(random.choices(string.digits,k=8)),
            "fullName":get_random_string(30),
            "email" :get_random_string(10)+'@mail.com',   
        })
    for i in range(10):
        people=random.choice(peoples)
        args={
            "dni":people["dni"],
            "fullName":people["fullName"],
            "email" :people["email"],
            "type" : "I"     
        }
        movement=Movement(**args)
        db.session.add(movement)
        db.session.commit()
        for j in range(10):
            args={
                "moveId" :movement.id,
                "marca":random.choice(marks),
                "denomination":get_random_string(30),
                "condition":random.choice(conditions)
            }
            movementDet=MoveDetail(**args)
            db.session.add(movementDet)  
    db.session.commit()
    return jsonify(str(True))


# A decorator that is used to define the route for the function.
#If the user is authenticated, then merge the json object into the database and return a json object
# with a value of 1   
# :param user: the user object that is returned by the token_required decorator
# :return: The return value of the decorated function.
@app.route('/',methods=['PUT'])
@token_required
def move_put(user):
    o=request.json
    print (user)
    db.session.merge(o)
    db.session.commit()
    return _json(1)

# It deletes the movement.
# :param ids: The id of the movement to be deleted
# :return: The return value of the function.
@app.route('/<ids>',methods=['DELETE'])
@token_required
def move_delete(user,ids):
    print (user)
    for moveId in ids.split(','):
        moveId=int(moveId)
        movement = Movement.query.get(moveId)
        movement.canceled=1
        db.session.merge(movement)
    if id ():
        message.filter_by(fullname=id) 
        db.session = request.args.get(db.session)
    if db.session():
        message.filter_by(db.session)
    if move_detail ():
        message.filter_by(move_detasil= move_detail)
    db.session.delete(move_detail)
    db.session.commit()
    return _json(1)

# It returns a json with the size of the query and the data of the query.
# :param moveId: the id of the movement
# :return: A list of MoveDetail objects
@app.route('/<moveId>/detail')
@token_required
def move_detail(user,moveId):
    print(user)
    page=int(page)
    size=int(size)
    codePatrimonial = request.args.get("codePatrimonial")
    offset=(page*size)
    limit=(size*(page+1))
    query=MoveDetail.query
    if codePatrimonial:
        codePatrimonial = "%{}%".format(codePatrimonial)
        query=query.filter(MoveDetail.codePatrimonial.like(codePatrimonial))
    size= query.count()
    moveDetails = query.offset(offset).limit(limit).all()
    result = movement_schema.dump(moveDetails)
    data = {
        'size':size,
        'data':result
    }
    return _json(data)

# It takes a POST request with a JSON object containing a code, and returns a JSON object containing
# an access token
# :return: {
#   "error": "invalid_grant",
#   "error_description": "Invalid authorization code: "
# }
@app.route('/token',methods=['POST'])   
def token_post():
    o=request.json
    try:    
        code=o['code']
        reqUrl = "http://web.regionancash.gob.pe/api/oauth/token"
        headers = {
            'Authorization': 'Basic {}'.format(
                base64.b64encode(
                '{username}:{password}'.format(
                    username=os.environ.get('OAUTH_CLIENT_ID', ''),
                    password=os.environ.get('OAUTH_CLIENT_SECRET', '')
                ).encode()
                ).decode()
            ),
        }
        response = requests.post(reqUrl, data={'grant_type': 'authorization_code','scope':'profile','code':str(code)},  headers=headers)
        o=json.loads(response.content)
        return o
    except Exception as e:
        return jsonify(str(e))
 
# It takes a JSON object, creates a dictionary from it, and then creates a Movement object from the
# dictionary.
# :return: The object that was created.
@app.route('/in',methods=['POST'])
@token_required
def in_post(user):
    print(user)
    o=request.json
    try:    
        values = {}
        for x in get_attrs(Movement):
            try:
                values[x]=o[x]
                if x=='date':
                    values[x]=datetime.strptime(values[x], '%Y-%m-%d %H:%M:%S')
            except KeyError:
                print("Variable "+x+" is empty")
        movement=Movement(**values)
        db.session.add(movement)
        db.session.commit()
        return _json(MoveSchema().dump(movement))
    except Exception as e:
        return jsonify(str(e))
     
# It takes a JSON object, creates a MoveDetail object, and adds it to the database.
# :return: The object that was created.
@app.route('/detail',methods=["POST"])
@token_required
def detail_post(user):
    print(user)
    o=request.json
    try:        
        values = {}
        for y in get_attrs(MoveDetail):
            try:
                values[y]=o[y]
            except KeyError:
                print("Variable "+y+" is empty")
        moveDetail=MoveDetail(**values)
        db.session.add(moveDetail)
        db.session.commit()
        return _json(MoveSchema().dump(moveDetail))
    except Exception as e:
        return jsonify(str(e))

# It takes a moveId, gets the movement and its details from the database, expunges them from the
# session, dumps them into a dictionary, and returns the dictionary
@app.route('/url',)
@token_required
def get_data(user):
    print (user) 
    temp = tempfile.TemporaryFile()
    """with open () as f :
        f.write (stuff)""" 
    m=_move_get(1)
    m=[m]
    temp.write(jsonify(m).get_data(as_text=False))
    temp.seek(0)
    data=temp.read()
    temp.close()
    conten =  requests.post('http://web.regionancash.gob.pe/api/jreport/', 
        files={'file':data },
        data={'filename': 'data.json','template':'pad'}).content
    return Response(conten, mimetype='application/pdf')
def _move_get(moveId):
    try:
        int(moveId)
    except Exception as e:
        print(e)
        return None
    moveId=int(moveId)
    print('moveId='+str(moveId))
    movement = Movement.query.get(moveId)
    if not movement==None:
        print('movement='+str(movement))
        details=movement._details
        db.session.expunge(movement)
        for detail in details:
            db.session.expunge(detail)
        movementSchema = MoveSchema()   
        movement=movementSchema.dump(movement)
        moveDetailSchema = MoveDetailSchema(many=True) 
        movement['details']=moveDetailSchema.dump(details)
        print(movement)
    return movement

# It takes a moveId as a parameter, and returns a json object containing the moveId, the moveName, and
# the moveDescription
# :param moveId: The ID of the move to get
# :return: A JSON object with the moveId and the moveName.
@app.route('/<moveId>')
@token_required
def move_get(user,moveId):
    print (user)
    m=_move_get(moveId)
    print(m)
    return jsonify(m)

# If the user requests the favicon.ico file, send it from the static folder.
# :return: The favicon.ico file is being returned.    
@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


# A decorator that is used to define the route for the function.
# It takes a user, prints the user, queries the database for all MoveDetails, counts the number of
# MoveDetails, creates a MoveDetailSchema, dumps the MoveDetails into the MoveDetailSchema, creates a
# dictionary with the size and the MoveDetailSchema, and returns a response with the dictionary
@app.route('/details/<offset>/<limit>',methods=["GET"])
@token_required
def detail_get(user,offset=0,limit=10):
    print(user)
    offset=int(offset)
    limit=int(limit)
    query=MoveDetail.query.filter()
    size= query.count()
    MoveDetails = query.offset(offset).limit(limit).all()

    moveDetailSchema = MoveDetailSchema(many=True) 
    result = moveDetailSchema.dump(MoveDetails)
    data = {
        'size':size,
        'data':result
        }
    return make_response(jsonify(data))


@app.route('/user/<document>',methods=["GET"])
@token_required
def user_get(user,document):
    try:        
        query=Movement.query.filter(or_(Movement.canceled == 0 , Movement.canceled == None  ))
        query=query.filter(Movement.dni.like(document))
        movements = query.offset(0).limit(1).all()
        if len(movements)==0:
            return {}
        movements=movements[0]
        return {'document':movements.dni,'fullname':movements.fullName,'email': movements.email}
    except Exception as e:
        return jsonify(str(e))


@app.route('/movement/<id>',methods=["GET"])
@token_required
def movement_get(user,id):
    print(user)
    try:        
        query=Movement.query.filter(or_(Movement.canceled == 0 , Movement.canceled == None  )) 
        moves = query.offset(0).limit(1).all()
        if len(moves)==0:
            return {}
        moves=moves[0]
        return {'dni':moves.dni,'fullname':moves.fullName,'email': moves.email, 'type': moves.type,'reason':moves.reason, ' document_authorization':moves. document_authorization,
                'dni_destino': moves.dni_destino,'fullName_destino':moves.fullName_destino, 'email_destino':moves.email_destino, 'proveedor_destino':moves.proveedor_destino,
                'local_destino': moves.local_destino,'adress_destino': moves.adress_destino,'id':moves.id}
    except Exception as d:  
        return jsonify(str(d))



@app.route('/movementd/<offset>/<limit>',methods=["GET"])
@token_required
def movements_get(user, offset=0,limit=10):
    offset = int(offset)
    limit= int (limit)
    if offset ==0 :        
        query=Movement.query.filter(or_(Movement.canceled == 0 , Movement.canceled == None  )) 
        size =query.count()
        moves = query.offset(offset).limit(limit).all()
        result = {'dni':moves.dni,'fullname':moves.fullName,'email': moves.email, 'type': moves.type,'reason':moves.reason, ' document_authorization':moves. document_authorization,
                'dni_destino': moves.dni_destino,'fullName_destino':moves.fullName_destino, 'email_destino':moves.email_destino, 'proveedor_destino':moves.proveedor_destino,
                'local_destino': moves.local_destino,'adress_destino': moves.adress_destino,'id':moves.id}
        data = {
            'size':size,
            'data':result
        }
    return jsonify(str(data))


@app.route('/details/traslate',methods=["GET"])
def detailss_get():


    return None