from fastapi import FastAPI
from app.routers import user
import dotenv

dotenv.load_dotenv()

app = FastAPI()

app.include_router(user.router, prefix="/user")

