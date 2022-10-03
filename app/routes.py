from concurrent.futures.process import _threads_wakeups
from app import app,db
from flask import request, jsonify
from app.auth_middleware import token_required
from app.models import get_attrs,Movement,movement_schema,MoveDetail,MoveDetailSchema,MoveSchema
from datetime import datetime
from email import message
from flask import  request ,make_response, Response,send_from_directory,jsonify
from sqlalchemy import or_
import tempfile
import os 
import requests



# ROUTES
# EndPoint 

# It takes a user object and returns a json response with the data  
# :param o: The object to be serialized
# :return: A response object
   
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

    if fullName:
        fullName = "%{}%".format(fullName)
        query=query.filter(Movement.fullName.like(fullName))
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



#

@app.route('/<idd>',methods=['PUT'])
@token_required
def move_put(user,ids):
    print (user)
    for moveId in ids.split(','):
        moveId=int(moveId)
        movement = Movement.query.get(moveId)
        movement.add=1
        db.session.merge(movement)

    db.session.commit()
    return _json(1)
#

# It deletes the movement.
# :param ids: The id of the movement to be deleted
# :return: The return value of the function.
@app.route('/<ids>',methods=['DELETE'])
def move_delete(ids):
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
def move_detail(moveId):
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



# It creates 10 Movement objects and 10 MovementDetail objects for each Movement object
# :return: A JSON object.
@app.route('/seed',methods=['GET'])
def seed():
    for i in range(10):
        args={
            "fullName":"fullname-"+str(i),
            "email" :"email-" +str(i),
        }
        movement=Movement(**args)
        db.session.add(movement)
        db.session.commit()
        for j in range(10):
            args={
                "moveId" :movement.id
            }
            movementDet=MoveDetail(**args)
            db.session.add(movementDet)  
    db.session.commit()
    return jsonify(str(True))


# It takes a POST request with a JSON object in the body, and returns the value of the 'code' key in
# the JSON object
# :return: <code>{
#   "code": "4/AAB-wQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ
@app.route('/token',methods=['POST'])    
def token_post():
    o=request.json
    try:    
        token=o['code']
        
        return str(token) 
    except Exception as e:
        return jsonify(str(e))


# It takes a JSON object, creates a dictionary from it, and then creates a Movement object from the
# dictionary.
# :return: The object that was created.
@app.route('/in',methods=['POST'])
def in_post():
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
        
        return str( movement) 
    except Exception as e:
        return jsonify(str(e))
     
# It takes a JSON object, creates a MoveDetail object, and adds it to the database.
# :return: The object that was created.
@app.route('/detail',methods=["POST"])
def detail_post():
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
        
        return str( moveDetail) 
    except Exception as e:
        return jsonify(str(e))



# It takes a json file, sends it to the server, and returns a pdf file
# :return: The response is a PDF file.
@app.route('/url',)
def get_data():
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

# It takes a movement id, gets the movement and its details from the database, expunges them from the
# session, then dumps them into a dictionary
# :param moveId: the id of the movement to be retrieved
# :return: A dictionary with the movement and details.
def _move_get(moveId):
    try:
        int(moveId)
    except Exception as e:
        print(e)
        return None
    moveId=int(moveId)
    movement = Movement.query.get(moveId)
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
def move_get(moveId):
    m=_move_get(moveId)
    print(m)
    return jsonify(m)




# If the user requests the favicon.ico file, send it from the static folder.
# :return: The favicon.ico file is being returned.    
@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
