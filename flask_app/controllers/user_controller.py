from flask import request, make_response, abort, Response
from flask_app import app
from flask_app.services import account_service, token_service, sanitization_service

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
    response = token_service.make_usertoken_response(response_data, user_id)
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
    response = token_service.make_usertoken_response(response_data, user_id)
  else:
    response = make_response(response_data)
  return response

@app.route('/api/renew-token', methods=['POST'])
def renew_token():
  try:
    decrypted_token = token_service.decrypt_token(request)
    user_id = decrypted_token['user_id']
    response_data = {'status': 'success', 'data': {}}
    response = token_service.make_usertoken_response(response_data, user_id)
    return response
  except:
    abort(Response("Please sign in.", 401))

@app.route('/api/logout')
def logout():
  response = make_response({'status': 'success', 'data': {'logoutRequest': 'Successfully logged out.'}})
  response.set_cookie('usertoken', value='', secure=True, httponly=True, expires=0)
  return response