# MaxAPI readme

### this app is an issue tracking system,we can register an account, create projects and add users as contributors to our projects where they can create issues as well as comment on issues (as long as they are contributors of said project).


## Configuration:

You will need two things before anything:
1. clone this github repository anywhere in your computer.
1. [Postman Desktop Version](https://www.postman.com/downloads/)
1. Then make sure to have [Python 3.x](https://www.python.org/downloads/) (any python above python 3)

### open your command terminal:

1. cd in the repository
1. pipenv shell
1. pip install -r requirements.txt 
1. python manage.py runserver

### open postman desktop version (from the [link](https://app.getpostman.com/join-team?invite_code=744e91417ef59c738b2cfa3892c7ffab&target_code=c7098eac84cd4a3ec8e2bccceeceeffa) given):
1. register a new account or direct login (with the default user data already given in the body)
1. once the login post done you need to copy either the access token or refresh token (access token is valid for 60 minutes while the refresh token is valid for 1day)
1. then you need to paste the token into the authorization tab of the 'maxapi' folder (type=bearer token)
1. You should be ready to test now
