from flask import Flask

app = Flask(__name__)


@app.route('login/')
def login():
    return '<p>login</p>'


@app.route('tree/create/')
def create_tree():
    return '<p>create</p>'


@app.route('tree/change/')
def change_tree():
    return '<p>change</p>'


@app.route('tree/delete/')
def delete_tree():
    return '<p>delete</p>'
