from fastapi import FastAPI, HTTPException
from typing import Union


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World..."}