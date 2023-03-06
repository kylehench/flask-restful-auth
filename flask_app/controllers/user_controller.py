from flask_app import app
from flask_app.services import account_service
from flask_app.services import sanitization_service
from flask import request, make_response
import jwt, datetime

def make_usertoken_response(response_data, user_id):
  usertoken = jwt.encode(
    { 'user_id': user_id,
      'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=28)
    },
    app.SECRET_KEY,
    algorithm="HS256"
  )
  response = make_response(response_data)
  response.set_cookie(
    key='usertoken',
    value=usertoken,
    secure=True,
    httponly=True,
    expires=datetime.datetime.utcnow() + datetime.timedelta(days=28)
  )
  return response

# routes
@app.route('/api/register', methods=['POST'])
def register():
  response_data, user_id = account_service.create_account(
    sanitized_username = sanitization_service.strip_xss(request.json.get('username')),
    sanitized_email = sanitization_service.strip_xss(request.json.get('email')),
    password = request.json.get('password'),
    password_confirm = request.json.get('password_confirm'),
  )
  if response_data['status'] == 'success':
    response = make_usertoken_response(response_data, user_id)
  else:
    response = make_response(response_data)
  return response

@app.route('/api/login', methods=['POST'])
def login():
  response_data, user_id = account_service.login(
    sanitized_email = sanitization_service.strip_xss(request.json.get('email')),
    password = request.json.get('password'),
  )
  if response_data['status'] == 'success':
    response = make_usertoken_response(response_data, user_id)
  else:
    response = make_response(response_data)
  return response

@app.route('/api/logout')
def logout():
  response = make_response({'status': 'success', 'data': {'logoutRequest': 'Successfully logged out.'}})
  response.set_cookie('usertoken', value='', secure=True, httponly=True, expires=0)
  return response