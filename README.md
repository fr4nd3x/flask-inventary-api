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

pip install mysql-connector-python 

pip install flask-sqlalchemy 

pip freeze > requirements.txt