import os, jwt
from flask import make_response
from flask_app import app
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
load_dotenv()

def decrypt_token(request):
  decrypted_token = jwt.decode(
    request.cookies.get('usertoken'),
    os.environ.get('SECRET_KEY'),
    algorithms="HS256"
  )
  # check that token has not expired
  expires = datetime.fromisoformat(decrypted_token['expires'])
  if expires < datetime.now(timezone.utc):
    raise PermissionError()
  return decrypted_token

def make_usertoken_response(response_data, user_id):
  expires = (datetime.now(timezone.utc) + timedelta(days=28)).replace(microsecond=0)
  expires_iso = expires.isoformat()
  usertoken = jwt.encode(
    { 'user_id': user_id,
      'expires' : expires_iso
    },
    app.SECRET_KEY,
    algorithm="HS256"
  )
  response_data['data']['token_expires'] = expires_iso
  response = make_response(response_data)
  response.set_cookie(
    key='usertoken',
    value=usertoken,
    secure=True,
    httponly=True,
    expires=expires_iso
  )
  return response