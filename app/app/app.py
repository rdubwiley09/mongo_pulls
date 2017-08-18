from flask import Flask, request, session, abort
from flask_restful import Api
from flask_bootstrap import Bootstrap
from flask_session import Session

app = Flask(__name__)
app.config.from_pyfile('config.py')

app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

Session(app)

Bootstrap(app)
