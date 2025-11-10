from fastapi import APIRouter
from config.db import conn
from models.index import users
from schemas.user import User  # assuming schema file is schemas/user.py

user = APIRouter()

@user.get("/")
async def read_users():
    result = conn.execute(users.select()).fetchall()
    return result


@user.get("/{id}")
async def read_user(id: int):
    result = conn.execute(users.select().where(users.c.id == id)).fetchone()
    return result



@user.post("/")
async def create_user(user: User):
    conn.execute(users.insert().values(
        name=user.name,
        email=user.email,
        password=user.password
    ))
    conn.commit()
    return conn.execute(users.select()).fetchall()


@user.put("/{id}")
async def update_user(id: int, user: User):
    conn.execute(users.update().values(
        name=user.name,
        email=user.email,
        password=user.password
    ).where(users.c.id == id))
    conn.commit()
    return conn.execute(users.select().where(users.c.id == id)).fetchone()



@user.delete("/{id}")
async def delete_user(id: int):
    conn.execute(users.delete().where(users.c.id == id))
    conn.commit()
    return conn.execute(users.select()).fetchall()
