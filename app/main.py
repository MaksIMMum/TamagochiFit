from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine, get_db
from app.routes import auth, pages, pet, workout, social, food
from app.models import User, Pet  # Import all models for Alembic awareness
from config import settings
from app.services.food_service import seed_shop



# Create database tables (fallback — migrations are the source of truth)
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="A Tamagotchi-style fitness tracking application",
    version="0.1.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict to specific domain before deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(auth.router)
app.include_router(pages.router)
app.include_router(pet.router)
app.include_router(workout.router)
app.include_router(social.router)

app.include_router(food.router)

@app.on_event("startup")
def startup():
    db = next(get_db())
    seed_shop(db)


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to TomogachiFit API",
        "version": "0.1.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}
