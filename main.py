from fastapi import FastAPI
from api.endpoints import contacts, birthdays

app = FastAPI()

app.include_router(contacts.router, prefix="/api")
app.include_router(birthdays.router, prefix="/api")
