import logging

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from presentation.routers import auth_router, project_router
from presentation.pages import auth_router_pages, project_router_pages


app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount('/static', StaticFiles(directory='../frontend/static', html=False))

app.include_router(auth_router, prefix='/api/v0')
app.include_router(project_router, prefix='/api/v0')
app.include_router(auth_router_pages)
app.include_router(project_router_pages)


if __name__ == '__main__':
    uvicorn.run('main:app')
