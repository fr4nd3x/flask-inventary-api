:: Int to pipenv and run a local host (http://localhost:5000/)
:: You must to put the letter "r".
::pipenv run flask --app app run
pipenv run waitress-serve wsqi:app
::pipenv run flask --app app run