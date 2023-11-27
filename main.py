from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session

app = Flask(__name__, template_folder='./app/templates', static_folder='./app/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pcharmacy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "My Secret key"
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

db = SQLAlchemy(app)
app.app_context().push()
migrate = Migrate(app, db, command='migrate')
sess = Session()




