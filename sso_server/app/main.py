from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routes import login_router, token_router, admin_router
from .middleware import SSOMiddleware
from .config import Config
from .sessions import SessionStore

app = FastAPI(title="Simple SSO Server")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Add middleware
config = Config()
app.add_middleware(SSOMiddleware, config=config)

# Routes
app.include_router(login_router, prefix="/auth", tags=["Authentication"])
app.include_router(token_router, prefix="/token", tags=["Token"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])

@app.get("/")
async def home():
    return {"message": "SSO Server is running"}