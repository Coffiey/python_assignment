from models import financial_data
from financial.api_controller import get_all_financial_data, get_financial_data_page,statistics
from flask import Blueprint


api_bp = Blueprint('api', __name__)

# This route will return a table of the whole database
@api_bp.route("/financial_data/all")
def all():
    response = get_all_financial_data()
    return f"{response}"

#this route will return 
@api_bp.route("/financial_data")
def finance():
    response = get_financial_data_page()
    return f"{response}"


@api_bp.route("/statistics")
def get_statistics():
    response = statistics()
    return f"{response}",200

