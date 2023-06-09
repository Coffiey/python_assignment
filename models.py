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
