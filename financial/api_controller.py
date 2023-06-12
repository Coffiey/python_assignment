from models import financial_data, db
from flask import request
from datetime import datetime, timedelta
from flask import jsonify


def get_all_financial_data():
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


def save_financial_data(data_list):
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
    #creates Start Date of search (default is today)
    start_date = request.args.get('start_date',default='1970-01-01', type=str)
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()

    #creates End day of search (default is Unix epoch)
    end_date = request.args.get('end_date',  default=(datetime.now().strftime('%Y-%m-%d')), type=str)
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

    #will send error if start date is later than end date
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
    
    # symbol is defined (return all results is symbol is not provided)
    symbol = request.args.get('symbol', default=False, type=str)

    # page number for pagination
    page = request.args.get('page', default=1, type=int)

    # limit oon items per page
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
     #creates Start Date of search (default is today)
    start_date = request.args.get('start_date',default='1970-01-01' , type=str)
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()

    #creates End day of search (default is Unix epoch)
    end_date = request.args.get('end_date',default=(datetime.now().strftime('%Y-%m-%d')) , type=str)
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
    
    # symbol is defined (return all results is symbol is not provided)
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
        # fetchs all data with the symbol
        all_data =  financial_data.query.filter_by(symbol=symbol)

        #this dictonary will store the total value of all values between the two date
        total_data = {
            "total_daily_open_price": 0,
            "total_daily_close_price": 0,
            "total_daily_volume": 0,
            "total_count": 0
        }

        #this loop will create a dict 
        for data in all_data:
        #     if start_date_obj <= data.date <= end_date_obj:
        #         total_data["total_daily_open_price"] = total_data["total_daily_open_price"] + data.open_price
        #         data_dict = {
        #             'id': data.id,
        #             'symbol': data.symbol,
        #             'date': data.date.strftime('%Y-%m-%d'),
        #             'open_price': data.open_price,
        #             'close_price': data.close_price,
        #             'volume': data.volume
        #         }
        #         data_list.append(data_dict)
        # return total_data
        
            # print(data)
            if start_date_obj <= data.date <= end_date_obj:
                total_data["total_daily_open_price"] = total_data["total_daily_open_price"] + data.open_price
                total_data["total_daily_close_price"] = total_data["total_daily_close_price"] + data.close_price
                total_data["total_daily_volume"]= total_data["total_daily_volume"] + data.volume
                total_data["total_count"] = total_data["total_count"] + 1
                    

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
