import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

load_dotenv(override=True)

THREADS_CLIENT_SECRET = os.getenv("THREADS_CLIENT_SECRET")
THREADS_APP_ID = os.getenv("THREADS_APP_ID")
THREADS_APP_SECRET = os.getenv("THREADS_APP_SECRET")
THREADS_API_URL = os.getenv("THREADS_API_URL")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/auth", response_class=HTMLResponse)
def read_index():
    with open(os.path.join("static", "index.html")) as f:
        return HTMLResponse(content=f.read())


@app.get("/auth/callback", response_class=HTMLResponse)
def read_callback():
    with open(os.path.join("static", "index.html")) as f:
        return HTMLResponse(content=f.read())


@app.get("/")
def read_root():
    return {"Hello": "World"}


class TokenRequest(BaseModel):
    code: str
    redirect_uri: str


@app.post("/access-token")
def get_token(request: TokenRequest):
    payload = {
        "client_id": THREADS_APP_ID,
        "client_secret": THREADS_APP_SECRET,
        "redirect_uri": request.redirect_uri,
        "code": request.code,
        "grant_type": "authorization_code",
    }

    try:
        response = requests.post(f"{THREADS_API_URL}/oauth/access_token", data=payload)
        response.raise_for_status()
        return JSONResponse(content=response.json())
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/long-lived-access-token")
def get_long_lived_token(access_token: str):
    params = {
        "grant_type": "th_exchange_token",
        "client_secret": THREADS_CLIENT_SECRET,
        "access_token": access_token,
    }

    try:
        response = requests.get(f"{THREADS_API_URL}/access_token", params=params)
        response.raise_for_status()
        return JSONResponse(content=response.json())
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))
