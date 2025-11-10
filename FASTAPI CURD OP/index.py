from fastapi import FastAPI
from routes.index import user
app = FastAPI()

app.include_router(user)
@app.get("/")
def read_root():
    return {"message": "Hello Kashish!"}
