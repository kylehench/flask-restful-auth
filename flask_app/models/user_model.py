from flask_app.config.mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9_-]+$')

class User:
  db_name = 'flask-restful-auth'

  def __init__(self, data):
    self.id = data['id']
    self.username = data['username']
    self.email = data['email']
    self.password = data['password']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']

  @staticmethod
  def validate_password(unhashed_password, password_confirm):
    if not unhashed_password:
      raise ValueError('Please enter a password.')
    if len(unhashed_password) < 8:
      raise ValueError('Password must contain at least 8 characters.')
    if not password_confirm:
      raise ValueError('Please confirm your password.')
    if unhashed_password != password_confirm:
      raise ValueError('Passwords do not match.')
    return True

  @staticmethod
  def validate_sanitized_email(sanitized_email):
    if not sanitized_email:
      raise ValueError('Please enter an email address.')
    if not EMAIL_REGEX.match(sanitized_email):
      raise ValueError('Please enter a valid email address.')
    query = 'SELECT 1 FROM users WHERE email=%(email)s;'
    users = connectToMySQL(User.db_name).query_db(query, {'email': sanitized_email})
    if len(users) > 0:
      raise ValueError('Email already registered.')
    return True

  @staticmethod
  def validate_sanitized_username(sanitized_username):
    if not sanitized_username:
      raise ValueError('Please enter a username.')
    if not (2 < len(sanitized_username) < 16):
      raise ValueError('Username must be 3-15 characters long.')
    if not USERNAME_REGEX.match(sanitized_username):
      raise ValueError('Username may only contain characters, numbers, hypens, and/or underscores.')
    query = 'SELECT 1 FROM users WHERE username=%(username)s;'
    users = connectToMySQL(User.db_name).query_db(query, {'username': sanitized_username})
    if len(users) > 0:
      raise ValueError('Username already exists.')
    return True

  @classmethod
  def create(cls, sanitized_email, sanitized_username, hashed_password):
    query = 'INSERT INTO users (username, email, password) VALUES ( %(username)s , %(email)s , %(password)s )'
    user_id = connectToMySQL(cls.db_name).query_db(query, {'username': sanitized_username, 'email': sanitized_email, 'password': hashed_password})
    if not user_id:
      raise SystemError('Failed to create user in database.')
    return user_id

  @classmethod
  def get_by_email(cls, sanitized_email):
    query = 'SELECT * FROM users WHERE email= %(email)s ;'
    results = connectToMySQL(cls.db_name).query_db(query, {'email': sanitized_email})
    if len(results) < 1:
      raise ValueError('User not found.')
    return cls(results[0])