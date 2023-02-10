from flask_app import app
from flask_app.models import user_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


def hash_password(password):
  return bcrypt.generate_password_hash(password, rounds=9)

def add_error(response_data, category=None, error=None):
  # changes value of status to fail and optionally adds category and message from error object
  response_data['status'] = 'fail'
  if 'errors' not in response_data['data']:
    response_data['data']['errors'] = {}
  if category and error:
    response_data['data']['errors'][category] = error.args[0]

def create_account(sanitized_username, sanitized_email, password, password_confirm):
  response_data = {'status': 'success', 'data': {}}
  user_id = None

  # validate username
  try:
    user_model.User.validate_sanitized_username(sanitized_username)
  except ValueError as e:
    add_error(response_data, 'username', e)
  
  # validate password
  try:
    user_model.User.validate_password(password, password_confirm)
  except ValueError as e:
    add_error(response_data, 'password', e)

  # validate email
  try:
    user_model.User.validate_sanitized_email(sanitized_email)
  except ValueError as e:
    add_error(response_data, 'email', e)

  # return if any validation errors
  if response_data['status']=='fail':
    return response_data, user_id

  # create account
  hashed_password = hash_password(password)
  try:
    user_id = user_model.User.create(
      sanitized_email = sanitized_email,
      sanitized_username = sanitized_username,
      hashed_password = hashed_password
    )
    response_data['data']['username'] = sanitized_username
    response_data['data']['email'] = sanitized_email
  except SystemError:
    add_error(response_data, 'server', e)

  return response_data, user_id

def login(sanitized_email, password):
  response_data = {'status': 'success', 'data': {}}
  user, user_id = None, None

  # attempt to get user from database
  try:
    user = user_model.User.get_by_email(sanitized_email)
    user_id = user.id
  except ValueError as e:
    # user, user_id = None
    add_error(response_data)
  
  # if user found and password is correct, add email and username to response
  if user and bcrypt.check_password_hash(user.password, password):
    response_data['data']['username'] = user.username
    response_data['data']['email'] = user.email
  else:
    add_error(response_data, 'credentials', ValueError('Incorrect username or password.'))

  return response_data, user_id