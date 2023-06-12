from models import financial_data
from financial.api_controller import get_all_financial_data, get_financial_data_page,statistics
from flask import Blueprint
from flask import jsonify


api_bp = Blueprint('api', __name__)

@api_bp.route("/financial_data/all")
def all():
    """
    Retrieves all financial data.

    Returns:
        dict: A dictionary containing the financial data.

    """
    response = get_all_financial_data()
    return jsonify(response), 200


@api_bp.route("/financial_data")
def finance():
    """
    Retrieves financial data based on specified parameters.

    Returns:
        dict: A dictionary containing the financial data.

    """
    response = get_financial_data_page()
    return jsonify(response), 200


@api_bp.route("/statistics")
def get_statistics():
    """
    Retrieves statistics based on specified parameters.

    Returns:
        dict: A dictionary containing the statistics.

    """
    response = statistics()
    return jsonify(response), 200


@api_bp.errorhandler(404)
def handle_not_found_error(e):
    """
    Handles 404 (Not Found) errors.

    Returns:
        str: Error message.

    """
    return "Invalid route", 404

