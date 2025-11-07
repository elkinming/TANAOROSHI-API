from typing import Union
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
import random

from fastapi.responses import JSONResponse

from routers import inventory

# from models.user import User

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Routes Import
app.include_router(inventory.router)

# Function for getting the DB connection
def get_connection():

    db_config = {
        "host": "localhost",
        "port": 5432,
        "dbname": "koujyou_db",
        "user": "postgres",
        "password": "Elkinpg1"
    }

    return psycopg2.connect(**db_config)

