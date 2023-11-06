from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import FastAPI

from routers import predict
import os

SERVER_URL = "localhost"

app = FastAPI(root_path='/api')

# CORS
origins = [SERVER_URL]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import modules
app.include_router(
    predict.router,
    prefix="/predict",
    tags=["predict"]
)