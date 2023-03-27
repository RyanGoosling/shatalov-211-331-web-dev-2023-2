from flask import Flask

app = Flask(__name__)
application = app

@app.route('/')#set FLASK_APP=app.py set FLASK_DEBUG=1
def index():
    return 'Hello, world! <3'
