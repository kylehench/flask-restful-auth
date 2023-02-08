from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
  db_name = 'flask-restful-auth'

  def __init__(self, data):
    self.id = data['id']
    self.username = data['username']
    self.email = data['email']
    self.password = data['password']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']

  # @staticmethod
  # def validate(data):
  #   response = {'status': 'success', 'data': {}}
  #   query = 'SELECT 1 FROM users WHERE email=%(email)s;'
  #   result = connectToMySQL(User.db_name).query_db(query, data)
  #   if len(res) > 0:
  #     return {'status': 'fail', data: }

  @classmethod
  def create(cls, data):
    response = {'status': 'success', 'data': {}}
    query = 'INSERT INTO users (username, email, password) VALUES ( %(username)s , %(email)s , %(password)s )'
    result = connectToMySQL(cls.db_name).query_db(query, data)
    if len(result)==1:
      response['data'] = {'user_id': result[0]}
    else:
      response['status'] = 'fail'
      return response