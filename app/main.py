from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import auth
app = FastAPI(title="TomogachiFit")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router)



@app.get("/")
async def root():
    return {"message": "Go to /login to see the page"}
