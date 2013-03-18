from flask import Flask, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.setup_app(app)

import models, views

@app.before_request
def before_request():
    g.db = db
    g.db_connection = db.engine.connect()
