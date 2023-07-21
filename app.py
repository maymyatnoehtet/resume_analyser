#!/usr/bin/env python
# coding: utf-8

from flask import Flask
from views import views
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

@app.template_filter('round_to_decimal')
def round_to_decimal(value, decimals=0):
    try:
        return round(float(value), decimals)
    except (ValueError, TypeError):
        return value

app.register_blueprint(views)

if os.getenv('ENVIRONMENT') == "production":
    port = os.getenv('PROD_PORT')
    host = os.getenv('PROD_HOST')
    debug = False
else:
    port = os.getenv('DEV_PORT')
    host = os.getenv('DEV_HOST')
    debug = True

if __name__ == "__main__":
  app.run(debug=debug, port=port, host=host)