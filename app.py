from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
import os
from model import financial_data
from dotenv import load_dotenv
from get_raw_data import get_financial_data
from flask_migrate import Migrate

API_KEY = os.environ.get('API_KEY')



app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://your_user:your_password@db:5432/your_database'
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# with app.app_context():
#     db.create_all()



@app.route('/')
def hello_world():
    print(os.environ.get('PASSWORD'))
    return render_template('index.html')
    # return "hello"

@app.route('/hello')
def hello():
    stock_symbol = "IBM"
    return f"{get_financial_data(stock_symbol)}"
    # return "hello"
