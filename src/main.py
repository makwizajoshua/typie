from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from routers.auth import router as auth_router
from routers.chatroom import router as ch_router
from routers.message import router as msg_router

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


@app.get("/health")
def health():
    return {"status": "ok"}
