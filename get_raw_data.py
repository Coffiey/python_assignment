import requests
from datetime import datetime, timedelta

symbol = "IBM"
apiKey="RE84XSIRXVWO1NH0"
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=AAPL&outputsize=compact&apikey={apiKey}'
r = requests.get(url)
data = r.json()
day_data = data['Time Series (Daily)']
current_date = datetime.now().date()
two_weeks_ago = current_date - timedelta(weeks=2)

data_obj = []
if r.status_code == 200:
    for day_obj in day_data:
        date_object = datetime.strptime(day_obj, "%Y-%m-%d").date()
        if date_object >= two_weeks_ago:
            data_obj.append({
                "symbol": symbol,
                "date": date_object,
                "open_price": day_data[day_obj]['1. open'],
                "close_price": day_data[day_obj]['4. close'],
                "volume": day_data[day_obj]['6. volume'],
            })
print(data_obj)



# print(data['Time Series (Daily)'])

