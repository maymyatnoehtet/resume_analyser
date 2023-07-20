#!/usr/bin/env python
# coding: utf-8

from flask import Flask
from views import views

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.register_blueprint(views, url_prefix="/views")

if __name__ == "__main__":
  app.run(debug=True, port=3000)