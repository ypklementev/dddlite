from fastapi import FastAPI
from api.report import router

app = FastAPI()
app.include_router(router)