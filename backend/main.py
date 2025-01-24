import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from presentation.routers import auth_router, project_router, task_router


app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix='/api/v0')
app.include_router(project_router, prefix='/api/v0')
app.include_router(task_router, prefix='/api/v0')


if __name__ == '__main__':
    uvicorn.run('main:app')
