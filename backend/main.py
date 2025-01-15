import uvicorn
from fastapi import FastAPI
from api.routers import all_routers
from starlette.middleware.cors import CORSMiddleware
import argparse

app = FastAPI(
    title="Unit Of Work & FastAPI Users"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # "*" allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

for router in all_routers:
    app.include_router(router)