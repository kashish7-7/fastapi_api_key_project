from routes.user import user
from routes.index import user

app = FastAPI()

app.include_router(user)