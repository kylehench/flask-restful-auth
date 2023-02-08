# flask-restful-auth

## Deployment
Instructions for deployment on a Linux server with Node, PM2, Python 3, PIP, VENV, MySQL, and Nginx installed.
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pipenv
Clone project from GitHub, create virtual environment, and install modules
```
git clone https://github.com/kylehench/flask-restful-auth
cd flask-restful-auth
python3 -m venv venv
source venv/bin/activate
python -m pip install gunicorn
pipenv install

```