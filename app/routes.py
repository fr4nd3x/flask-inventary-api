from concurrent.futures.process import _threads_wakeups
from app import app,db
from flask import request, jsonify,url_for
from app.auth_middleware import token_required
from app.models import get_attrs,Movement,movement_schema,MoveDetail,MoveDetailSchema,MoveSchema
from datetime import datetime
from email import message
from flask import jsonify, request ,make_response, Response
from sqlalchemy import or_
import tempfile
import requests


@app.route('/<offset>/<limit>')
@app.route('/index')
@token_required
def index(user,offset=0,limit=50):
    print(user)
    offset=int(offset)
    limit=int(limit)
    fullName = request.args.get("fullName")
    query=Movement.query.filter(or_(Movement.canceled == 0 , Movement.canceled == None  ))


    if fullName:
        fullName = "%{}%".format(fullName)
        query=query.filter(Movement.fullName.like(fullName))
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


    for moveId in ids.split(','):
        moveId=int(moveId)
        movement = Movement.query.get(moveId)
        movement.add=1
        db.session.merge(movement)

    db.session.commit()
    return _json(1)

#


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


@app.route('/token',methods=['POST'])
def token_post():
    o=request.json
    try:    
        token=o['code']
        
        return str( token) 
    except Exception as e:
        return jsonify(str(e) )

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
        return jsonify(str(e) )
     
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


@app.route('/url',)
def get_data():
    #SaveToFile(move_get(5).get_data(as_text=True).'data.json')
    temp = tempfile.TemporaryFile()
    """with open () as f :
        f.write (stuff)""" 
    m=_move_get(5)
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
    movement = Movement.query.get(moveId)
    details=movement._details
    db.session.expunge(movement)
    for detail in details:
        db.session.expunge(detail)
    movementSchema = MoveSchema()   
    movement=movementSchema.dump(movement)
    moveDetailSchema = MoveDetailSchema(many=True) 
    movement['details']=moveDetailSchema.dump(details)
    return movement

@app.route('/<moveId>')
def move_get(moveId):
    return jsonify(_move_get(moveId))
