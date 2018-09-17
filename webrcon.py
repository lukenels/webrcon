
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello world"

def create_app():
    return app
