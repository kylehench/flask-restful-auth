# flask-restful-auth

## Deployment
Instructions for deployment on a Linux server with Node, PM2, Python 3, PIP, VENV, MySQL, and Nginx installed.
Clone project from GitHub, create virtual environment, and install modules.
```
git clone https://github.com/kylehench/flask-restful-auth
cd flask-restful-auth
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
pip install gunicorn
```
Create a wsgi.py file with the contents:
```
from server import app as application
if __name__ == "__main__":
  application.run()
```
Test Server:
```
gunicorn --bind 0.0.0.0:5000 wsgi:application
```

Create a .env file in flask_app modeled off .env.example