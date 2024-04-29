from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)

@app.cli.command('init-db')
def init_db():
    """Create database tables from SQLAlchemy models."""
    db.create_all()
    print("Database initialized!")

from app import routes, models