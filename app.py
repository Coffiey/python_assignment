from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
import os
from models import financial_data, db
from dotenv import load_dotenv
from get_raw_data import get_financial_data
from flask_migrate import Migrate
from financial.api import api_bp
from financial.api_controller import save_financial_data, get_all_financial_data

API_KEY = os.environ.get('API_KEY')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_user:your_password@db:5432/your_database'
migrate = Migrate(app, db)

with app.app_context():
    db.init_app(app)
    db.create_all()

#redirects /api calles to the api router
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def hello_world():
    """
    Updates the database with financial data from AlphaVantage API.

    renders:
     -html page
    """
    stock_symbol = ["IBM","AAPL"]
    for stock in stock_symbol:
        answer = get_financial_data(stock)
        save_financial_data(answer)
    return render_template('index.html')
