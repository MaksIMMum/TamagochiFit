from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
async def login_submit(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "1234":
        message = "Login Successful! Welcome, Admin."
        msg_type = "success"
    else:
        message = "Invalid credentials. Try 'admin' and '1234'."
        msg_type = "danger"

    return templates.TemplateResponse("login.html", {
        "request": request,
        "message": message,
        "msg_type": msg_type
    })

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register", response_class=HTMLResponse)
async def register_submit(request: Request, username: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    if password != confirm_password:
        message = "Passwords do not match."
        msg_type = "danger"
    else:
        message = f"User '{username}' registered successfully!"
        msg_type = "success"

    return templates.TemplateResponse("register.html", {
        "request": request,
        "message": message,
        "msg_type": msg_type
    })
