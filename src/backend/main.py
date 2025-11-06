from fastapi import FastAPI

from backend.api import router

app = FastAPI(title="simple-backend")

app.include_router(router)
