from fastapi import FastAPI

from src.routes import contacts, auth

app = FastAPI()

app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "Hi! Welcome to the address book!"}
