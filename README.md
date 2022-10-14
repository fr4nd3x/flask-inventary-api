We work with flask CREATE A API WHIT FLASKA AND PYTHON

Create a folder:
mkdir flask-inventry-api

Go to the folder:
cd flask-inventry-api


Install a pipenv 
pip install pipenv


pipenv install

Whit pipenv, install flask 
pipenv install flask 

mkdir app 

touch app/__init__.py

touch app/routes.py

- In app/__init__.py:

    from app import app


172.16.1.1
--global http.proxy 172.16.1.1:port  

To connect a local host
pipenv shell 
flask --app main run


conexion bd 


pip freeze > requirements.txt
 waitress-serve 
web: waitress-serve wsqi:app



pip install mysql-connector-python 
pip install flask-sqlalchemy 
pip freeze
pip freeze > requirements.txt


vi Procfile
pip uninstall mysql-connector-python 
bd browser for sql lite 






// install heroku for windows

login heroku 
login heroku-i
proxi

172.16.1.1:3128

set HTTPS_PROXY=https://172.16.1.1:3128

Connect to heroku

heroku login 

set HTTPS_PROXY=https://proxy.server.com:portnumber

heroku git:remote https://inv2022.herokuapp.com/ | https://git.heroku.com/inv2022.git

heroku git:remote https://git.heroku.com/inv2022.git

heroku git:remote inv2022

Push to heroku 
git add .
git commit -am "Hello Meduim App"
git push heroku 

$ heroku git:remote -a <your-heroku-application-name>


when raise "Your Pipfile.lock is out of date. Expected"
-> pipenv lock

Delete Pipfile.lock

Install all dependences with pipenv (No run shell!)

pipenv install  flask-cors


https://inv2022.herokuapp.com/<offset>/<limit>


generate requirement.txt
pipenv lock -r > requirements.txt

https://developer.mozilla.org/es/docs/Learn/JavaScript/Objects/JSON

 create a new app in heroku 
 - heroku create example 

 curl -u ${client_id}:${client_secret} -XPOST http://web.regionancash.gob.pe/api/oauth/token-F grant_type=authorization_code -F scope=profile -F code=${code}

 
 @api.doc(params={"DNI":"dni", 
                "Type":"type",
                "Full Name":"fullName",
                "Email":"email",
                "Dependense":"dependence",
                "Company":"company",
                "Reference":"reference",
                "Date":"date"})