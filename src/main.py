from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.routers.auth_router import router as auth_router
from src.routers.chatroom_router import router as ch_router
from src.routers.message_router import router as msg_router

from .db import Base, engine

Base.metadata.create_all(engine)


templates = Jinja2Templates("templates/")
app = FastAPI(title="Typie")

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(msg_router)
app.include_router(ch_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/health")
def health():
    return {"status": "ok"}
