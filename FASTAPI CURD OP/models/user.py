from sqlalchemy import String, Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta

users = Table(
    'users',meta,
    column('id',Integer,primary_key=True),
    column('name',String(255)),
    column('email',String(255)),
    column('password',String(255)),
)


