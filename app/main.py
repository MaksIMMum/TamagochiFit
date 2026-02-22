from fastapi.staticfiles import StaticFiles
from app.routes import auth
from fastapi import FastAPI, APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI(title="TomogachiFit")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router)

@app.get("/")
async def root():
    return {"msg": "Go to /login to see the page"}
