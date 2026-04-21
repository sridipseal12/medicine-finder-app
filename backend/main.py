from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.routers import pharmacy_router

from app.routers import auth_router
from app.database import Base, engine
from app.models import user

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

# Serve static files (IMPORTANT)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(auth_router.router)
app.include_router(pharmacy_router.router)

# Homepage with image
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Medicine Finder</title>
        </head>
        <body style="text-align:center; font-family:sans-serif;">
            <h1>Medicine Finder API running</h1>
            <img src="/static/test.jpg" width="300"/>
        </body>
    </html>
    """