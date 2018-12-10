from bottle import run, Bottle, route, get, post 
from db import Contact, DB

def prepare():
    db = DB()
    app = Bottle()
    db.mountTo(app)
    return app

run(app = prepare(), host='localhost', port=8081, debug=True)