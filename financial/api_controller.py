from models import financial_data, db
from flask import request
from datetime import datetime, timedelta
from flask import jsonify

# This is a personal test route that is included for functionalilty testing, it is not requested by the assesment
def get_all_financial_data():
    """Gets financial Data from DB, selecting for start and end data, stock type, all parameters are optional

    Returns:
        list: List of data items.

    Raises:
        ValueError: If the page number or per_page value is invalid.
    """
    try:
        all_data = financial_data.query.all()
        data_list = []
        for data in all_data:
            data_dict = {
                'id': data.id,
                'symbol': data.symbol,
                'date': data.date.strftime('%Y-%m-%d'),
                'open_price': data.open_price,
                'close_price': data.close_price,
                'volume': data.volume
            }
            data_list.append(data_dict)
        return data_list
    except Exception as e:
        error_message = str(e)
        return {'error': error_message}


def save_financial_data(data_list):
    """Saves financial data to the database.

    Args:
        data_list (list): List of dictionaries containing financial data.

    Returns:
        bool: True if the data is successfully saved, False otherwise.

    Raises:
        Exception: If there is an error while saving the financial data.
    """
    try:
        for data in data_list:
            existing_data = financial_data.query.filter_by(symbol=data["symbol"], date=data["date"]).first()
            if existing_data:
                continue  # Skip saving if data already exists

            new_data = financial_data(
                symbol=data["symbol"],
                date=data["date"],
                open_price=float(data["open_price"]),
                close_price=float(data["close_price"]),
                volume=float(data["volume"])
            )
            db.session.add(new_data)

        db.session.commit()
        return True
    except Exception as e:
        return f"Error saving financial data: {str(e)}"


def get_financial_data_page():
    """Gets financial Data from DB, selecting for start and end data, stock type, all parameters are optional
    
    Args(from parpamters):
        start_date[str]: start of date limitation 
        end_date[str]: end of date limitation
        symbol[str]: stock option (IBM or AAPL)
    
    Retuns:
        dict: A dictionary containing paginated data.

        -"data" (list): List of data Items
        -"Paginination" (dict): Pagination information.

    Raises:
        ValueError: If the page number or per_page value is invalid.
        OrderError: If the Start date is later than the end date.
        """

    start_date = request.args.get('start_date',default='1970-01-01', type=str)
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = request.args.get('end_date',  default=(datetime.now().strftime('%Y-%m-%d')), type=str)
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

    if start_date_obj > end_date_obj:
        error_message = 'Start date cannot be later than the end date.'
        response = {
            'data': [],
            'pagination': {},
            'info': {
                'error': error_message
            }
        }
        return response
    
    symbol = request.args.get('symbol', default=False, type=str)
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=5, type=int)

    try:
        if symbol:
            pagination = financial_data.query.filter_by(symbol=symbol).paginate(page=page, per_page=limit)
        else:
            pagination = financial_data.query.paginate(page=page, per_page=limit)
        all_data = pagination.items

        data_list = []
        for data in all_data:
            if start_date_obj <= data.date <= end_date_obj:
                data_dict = {
                    'id': data.id,
                    'symbol': data.symbol,
                    'date': data.date.strftime('%Y-%m-%d'),
                    'open_price': data.open_price,
                    'close_price': data.close_price,
                    'volume': data.volume
                }
                data_list.append(data_dict)

        response = {
            'data': data_list,
            'pagination': {
                'count': pagination.total,
                'page': pagination.page,
                'limit': pagination.per_page,
                'pages': pagination.pages,
            },
            'info': {
                'error': ''
            }
        }

    except Exception as e:
        response = {
            'data': [],
            'pagination': {},
            'info': {
                'error': str(e)
            }
        }

    return response

def statistics():
    """Calculates statistics for financial data within a given date range and symbol.

    Args(from params):
        start_date (str): The start date of the date range in format 'YYYY-MM-DD'.
        end_date (str): The end date of the date range in format 'YYYY-MM-DD'.
        symbol (str): The stock symbol.

    Returns:
        dict: A dictionary containing the calculated statistics and error information.
        
        - "data" (dict): A dictionary containing the calculated statistics.
        - "info" (dict): A dictionary containing error information, if applicable.

    Raises:
        OrderError: If the start date is later than the end date.
        ValueError: If the end date is greater than today.
        Exception: If there is an error while calculating the statistics.
    """
    start_date = request.args.get('start_date',default='1970-01-01' , type=str)
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = request.args.get('end_date',default=(datetime.now().strftime('%Y-%m-%d')) , type=str)
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

    symbol = request.args.get('symbol', default=False, type=str)

    if start_date_obj > end_date_obj:
        error_message = 'Start date cannot be later than the end date.'
        response = {
            'data': [],
            'info': {
                'error': error_message
            }
        }
        return response
    try:
        all_data =  financial_data.query.filter_by(symbol=symbol)

        #this dictonary will store the total value of all values between the two date
        total_data = {
            "total_daily_open_price": 0,
            "total_daily_close_price": 0,
            "total_daily_volume": 0,
            "total_count": 0
        }

        #this loop will set total data
        for data in all_data:
            if start_date_obj <= data.date <= end_date_obj:
                total_data["total_daily_open_price"] = total_data["total_daily_open_price"] + data.open_price
                total_data["total_daily_close_price"] = total_data["total_daily_close_price"] + data.close_price
                total_data["total_daily_volume"]= total_data["total_daily_volume"] + data.volume
                total_data["total_count"] = total_data["total_count"] + 1
                    
        #this calcualtes the average aopen, close and volume across the selected paramters
        averaged_obj = {
            "start_date": start_date,
            "end_date":end_date,
            "symbol": symbol,
            "average_daily_open_price": total_data["total_daily_open_price"]/total_data["total_count"],
            "average_daily_close_price": total_data["total_daily_close_price"]/total_data["total_count"],
            "average_daily_volume": total_data[ "total_daily_volume"]/total_data["total_count"]
        }
        return {
            "data": averaged_obj,
            "info": {"error" : ''}
        }
    except Exception as e:
        return  {
            'data': [],
            'info': {
                'error': str(e)
            }
        }
