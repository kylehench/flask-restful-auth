from flask_app import app
from flask import request, make_response
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import jwt, datetime

# bcrypt = Bcrypt(app)

# move to Model
from flask_app.config.mysqlconnection import connectToMySQL

@app.route('/api/register', methods=['POST'])
def register():
  data = request.form.copy()
  print(data)
  data['password'] = bcrypt.generate_password_hash(data['password'])
  response = make_response({'some': 'data'})
  token = jwt.encode({'user_id': 'fake_id', 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.SECRET_KEY, algorithm="HS256")
  response.set_cookie('usertoken', value=token, secure=True, httponly=True)
  return response

@app.route('/api/login', methods=['POST'])
def login():
  return ''

@app.route('/logout')
def logout():
  return ''