from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
async def login_page():
    """Serve login page"""
    with open("app/templates/login.html", "r") as f:
        return f.read()

@router.get("/register", response_class=HTMLResponse)
async def register_page():
    """Serve registration page"""
    with open("app/templates/register.html", "r") as f:
        return f.read()

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page():
    """Serve dashboard page (requires authentication)"""
    with open("app/templates/dashboard.html", "r") as f:
        return f.read()


@router.get("/", response_class=HTMLResponse)
async def welcome_page():
    """welcome home page"""
    with open("app/templates/welcome_page.html", "r") as f:
        return f.read()
