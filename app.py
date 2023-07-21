#!/usr/bin/env python
# coding: utf-8

from flask import Flask
from views import views

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.template_filter('round_to_decimal')
def round_to_decimal(value, decimals=0):
    try:
        return round(float(value), decimals)
    except (ValueError, TypeError):
        return value

app.register_blueprint(views, url_prefix="/views")

if __name__ == "__main__":
  app.run(debug=True, port=3000)