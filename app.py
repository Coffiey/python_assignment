from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:database@localhost/finance'
db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return render_template('index.html')
    # return "hello"
