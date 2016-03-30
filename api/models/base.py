from api.app import db as DB
# from flask.ext.sqlalchemy import SQLAlchemy
# from app import app

# DB = SQAlchemy(app)

class BaseModel(DB.Model):
    __abstract__ = True
    id = DB.Column(DB.Integer, primary_key=True)
    created_at = DB.Column(DB.DateTime, default=DB.func.now())
    updated_at = DB.Column(DB.DateTime,
                           default=DB.func.now(),
                           onupdate=DB.func.now())
