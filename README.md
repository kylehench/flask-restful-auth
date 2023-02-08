# flask-restful-auth

## Deployment
Instructions for deployment on a Linux server with Node, PM2, Python 3, PIP, VENV, MySQL, and Nginx installed.
Install Linux packages:
```
sudo apt-get update
sudo apt-get install python3-pip nginx git -y
sudo apt-get install python3-venv -y
```
Create/update requirements.txt (if necessary). Then, commit and push to repo:
```
pipenv requirements > requirements.txt
```
Clone project from GitHub, create virtual environment, and install modules.
```
git clone https://github.com/kylehench/flask-restful-auth
cd flask-restful-auth
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
pip install gunicorn
```
Configure Gunicorn:
```
# /flask-restful-auth/wsgi.py
from server import app as application
if __name__ == "__main__":
  application.run()
```
Test Server:
```
gunicorn --bind 0.0.0.0:5000 wsgi:application
```

Create a .env file in flask_app modeled off .env.example