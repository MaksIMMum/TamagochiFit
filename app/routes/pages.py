from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
async def login_page():
    """Serve login page"""
    with open("app/templates/login.html", "r", encoding="utf-8") as f:
        return f.read()

@router.get("/register", response_class=HTMLResponse)
async def register_page():
    """Serve registration page"""
    with open("app/templates/register.html", "r", encoding="utf-8") as f:
        return f.read()

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page():
    """Serve dashboard page (requires authentication)"""
    with open("app/templates/dashboard.html", "r", encoding="utf-8") as f:
        return f.read()

@router.get("/shop", response_class=HTMLResponse)
async def shop():
    """shop"""
    with open("app/templates/shop.html", "r", encoding="utf-8") as f:
        return f.read()

@router.get("/leaderboard", response_class=HTMLResponse)
async def leaderboard_page():
    """Serve leaderboard page"""
    with open("app/templates/leaderboard.html", "r", encoding="utf-8") as f:
        return f.read()

@router.get("/meals", response_class=HTMLResponse)
async def meals_page():
    """Serve meals page"""
    with open("app/templates/meals.html", "r", encoding="utf-8") as f:
        return f.read()

@router.get("/", response_class=HTMLResponse)
async def welcome_page():
    """welcome home page"""
    with open("app/templates/welcome.html", "r", encoding="utf-8") as f:
        return f.read()

@router.get("/home", response_class=HTMLResponse)
async def home_page():
    """Serve home page"""
    with open("app/templates/home.html", "r", encoding="utf-8") as f:
        return f.read()

@router.get("/workouts", response_class=HTMLResponse)
async def workouts_page():
    """Serve workouts page"""
    with open("app/templates/workouts.html", "r", encoding="utf-8") as f:
        return f.read()

@router.get("/analysis", response_class=HTMLResponse)
async def analysis_page():
    """Serve analysis page"""
    with open("app/templates/analysis.html", "r", encoding="utf-8") as f:
        return f.read()



@router.get("/profile", response_class=HTMLResponse)
async def profile_page():
    """Serve profile page"""
    with open("app/templates/profile.html", "r", encoding="utf-8") as f:
        return f.read()

@router.get("/settings", response_class=HTMLResponse)
async def settings_page():
    """Serve settings page"""
    with open("app/templates/settings.html", "r", encoding="utf-8") as f:
        return f.read()


@router.get("/hatch", response_class=HTMLResponse)
async def hatch_page():
    """Serve hatch page"""
    with open("app/templates/hatch.html", "r", encoding="utf-8") as f:
        return f.read()
