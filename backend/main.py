import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from presentation.routers.auth_router import router as auth_router
from presentation.pages.account_pages import router as auth_router_pages

# to get a string like this run:
# openssl rand -hex 32


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
app.include_router(auth_router_pages)

if __name__ == '__main__':
    uvicorn.run('main:app')