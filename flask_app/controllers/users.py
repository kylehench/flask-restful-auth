from flask_app import app

from flask import request, render_template

@app.route('/test')
def test():
  return render_template('/users.html')