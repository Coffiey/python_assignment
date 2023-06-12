# Finance API

##prerequistes
Docker Desktop

### Directory structure

```
project-name/
├── model.py
├── migrations
├── get_raw_data.py
├── Dockerfile
├── docker-compose.yml
├── README.md
├── assignment.md
├── requirements.txt
├── template/
    ├── index.html
└── financial/
        ├──api_controler
        ├──api.py

```

### Available Routes

<ul>
    <li>"/" route :renders HTML home page</li>
    <li>/api/financial_data :fetches DB information for a selected stock between the two specified dates, all parameters are optional, if excluded, it will return data for all dates saved in DB, and for all stocks saved.
    <br/>params(optional):
        <ul>
            <li>start_date</li>
            <li>end_date</li>
            <li>symbol</li>
        </ul>
    </li>
    <li>/api/statistics will collect an average opending and closing price of a stock between the start and end date, if dates are excluded, it will return data for all dates saved in DB, 
    <br/>params(req):
        <ul>
            <li>symbol</li>
        </ul>
    <br/>params(optional):
        <ul>
            <li>start_date</li>
            <li>end_date</li>
        </ul>
    </li>
    <li>
    /financial_data :gets all Data from database.
    </li>
</ul>

## Run Docker Container

1. create a .env file for your api key
2. run the docker command

```
docker compose --build
```

Please note I am useing PostgreSQL for the DATABASE and not sqlite3, Becuase it is a postgreSQL database inside Docker Container there is no need to install PostgreSQL on your local device or create a user and password, this is all done by the App.
However: every so often, when creating a new image on init start up, the flask app can initalise and run before the postgreSQL Database is fully configured.
This is a bug under Investigation however due to time restraints and it only happining on the intial load I recomend simply running the comand ` docker compose --build` twice if a connection error is observed.

#interation
I have intergrated the DataBase update into the startUp of the Api and so there is no need to run the command
`~~python get_raw_data.py~~`
this step happens automatically on start up.

from here you can interact with the Data in one of two ways, make standard url calles
eg

```bash
'http://localhost:5000/api/financial_data?start_date=2023-01-01&end_date=2023-01-14&symbol=IBM&limit=3&page=2'

```

for financial Data

and

```bash
'http://localhost:5000/api/statistics?start_date=2023-01-01&end_date=2023-01-31&symbol=IBM'
```

for the statistics API

or for convience there is basic HTML protal on the route directory that you can visualise the data in a table.

### example of expected Data

for /api/financial_data:

```
{
    "data": [
        {
            "symbol": "IBM",
            "date": "2023-01-05",
            "open_price": "153.08",
            "close_price": "154.52",
            "volume": "62199013",
        },
        {
            "symbol": "IBM",
            "date": "2023-01-06",
            "open_price": "153.08",
            "close_price": "154.52",
            "volume": "59099013"
        },
        {
            "symbol": "IBM",
            "date": "2023-01-09",
            "open_price": "153.08",
            "close_price": "154.52",
            "volume": "42399013"
        }
    ],
    "pagination": {
        "count": 20,
        "page": 2,
        "limit": 3,
        "pages": 7
    },
    "info": {'error': ''}
}

```

for api/statistics:

```
{
    "data": {
        "start_date": "2023-01-01",
        "end_date": "2023-01-31",
        "symbol": "IBM",
        "average_daily_open_price": 123.45,
        "average_daily_close_price": 234.56,
        "average_daily_volume": 1000000
    },
    "info": {'error': ''}
}

```
