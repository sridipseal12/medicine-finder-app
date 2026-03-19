from fastapi import FastAPI
from app.routers import auth_router
from app.database import Base, engine
from app.models import user

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

# Include routers
app.include_router(auth_router.router)

@app.get("/")
def home():
    return {"message": "Medicine Finder API running"}