mkdir flask-inventry-api

cd flask-inventry-api

pip install pipenv

pipenv install

pipenv install flask 

mkdir app 

touch app/__init__.py

touch app/routes.py

- In app/__init__.py:

    from app import app


172.16.1.1
--global http.proxy 172.16.1.1:port  

pipenv shell 
pipenv 
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
heroku login 
set HTTPS_PROXY=https://proxy.server.com:portnumber

heroku git:remote https://inv2022.herokuapp.com/ | https://git.heroku.com/inv2022.git

heroku git:remote https://git.heroku.com/inv2022.git

heroku git:remote inv2022
git add .
git commit -am "Hello Meduim App"

$ heroku git:remote -a <your-heroku-application-name>


when raise "Your Pipfile.lock is out of date. Expected"
-> pipenv lock