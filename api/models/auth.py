from .base import BaseModel, DB
# from app import db as Db

class User(BaseModel):
    __tablename__ = 'users'
    nick = DB.Column(DB.String(100))
    pwd = DB.Column(DB.String(200))
    email = DB.Column(DB.String(150))

class Role(BaseModel):
    __tablename__ = 'roles'
    tag = DB.Column(DB.String(50))
    desc = DB.Column(DB.String(200))
