import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os


def get_financial_data(stock_symbol):
    #Fetches and processes Raw Data of selected Stock eg..."IBM"
    FUNCTION="TIME_SERIES_DAILY_ADJUSTED"
    API_KEY=os.environ.get("API_KEY")
    url = f'https://www.alphavantage.co/query?function={FUNCTION}&symbol={stock_symbol}&outputsize=compact&apikey={API_KEY}'

    #fetch request to alphaVantage
    response = requests.get(url)
    data = response.json()

    #formats Daily data and limits size to the last 14 results
    financial_data = data['Time Series (Daily)'][:14]
    two_weeks_ago = datetime.now().date() - timedelta(weeks=2)

    #creates Data-base formatted list
    financial_data_obj = []

    #iterates through the last 14 results 
    if response.status_code == 200:
        for day_obj in financial_data:
            date_object = datetime.strptime(day_obj, "%Y-%m-%d").date()
            if date_object >= two_weeks_ago:
                financial_data_obj.append({
                    "symbol": stock_symbol,
                    "date": date_object,
                    "open_price": financial_data[day_obj]['1. open'],
                    "close_price": financial_data[day_obj]['4. close'],
                    "volume": financial_data[day_obj]['6. volume'],
                })

    return financial_data_obj