from concurrent.futures.process import _threads_wakeups
#from crypt import methods
#from pydoc import render_doc
#flask --app main runfrom urllib import request
from app import app
from flask import request, jsonify,url_for




@app.route('/')
@app.route('/index')
def index():
    data={'id':1,'name':'mary222'}
    return jsonify(data)

@app.route('/in',methods=['POST'])
def in_post():
    return 1

@app.route('/out',methods=["POST"])
def out_post():
    return 1

@app.route('/detail',methods=["POST"])
def detail_post():
    return 1
    
@app.route('/movement',methods=["GET"])
def movement_get():
    data={'id':1,'name':'mary'}
    return jsonify(data)


##app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+mysqlconnector://grupoipe_python:grupoipe_python@s15.servidorlatinoamerica.com:3306/grupoipe_vetatrem'
#db = SQLAlchemy(app
#@app.route('/create/', methods=('GET', 'POST'))
#def create():
 #   if request.method == 'POST':
  #      firstname = request.form['firstname']
   #     lastname = request.form['lastname']
    #    email = request.form['email']
     #   age = int(request.form['age'])
      #  bio = request.form['bio']

       # return redirect(url_for('index'))

   # return render_template('create.html')

