
from flask import Flask, redirect

app = Flask(__name__)

@app.route('/')
def hello():
    return redirect('/static/hello.html')

def create_app():
    return app
