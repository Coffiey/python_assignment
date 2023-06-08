from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class financial_data(db.Model):
    __tablename__="financial_data"
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)
    open_price = db.Column(db.Integer, nullable=False)
    close_price = db.Column(db.Integer, nullable=False)
    volume = db.Column(db.Integer, nullable=False)


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


