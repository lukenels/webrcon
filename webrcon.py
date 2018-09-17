
from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route('/')
def hello():
    return app.send_static_file('hello.html')

def create_app():
    return app
