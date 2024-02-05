from fastapi import FastAPI
from uvicorn import run
from dotenv import load_dotenv
from database import Base, engine
from routers import user
from fastapi.middleware.cors import CORSMiddleware
import os
from starlette.middleware.sessions import SessionMiddleware

load_dotenv(dotenv_path=".env")

Base.metadata.create_all(bind=engine)
DOMAIN_NAME = os.environ.get("DOMAIN_NAME")
SECRET_KEY = os.environ.get("SECRET_KEY")
app = FastAPI(
    title="KnustAlumni23",
    description="Mini Project for KNUST Alumni to share their pictures and receive their congratulatory messages, instead of having to go through counless WhatsApp status updates and potentially missing some kind and inspiring words from friends and family.",
)
app.add_middleware(CORSMiddleware)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.secret_key = SECRET_KEY

app.include_router(user.router)

if __name__ == "__main__":
    run(app)
