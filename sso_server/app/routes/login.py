from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from ..auth import authenticate_user
from ..session import SessionStore
from ..tokens import create_code
from ..config import config
import hashlib

router = APIRouter()
templates = Jinja2Templates(directory="templates")
session_store = SessionStore()

@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def do_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    service_url: str = Form(None)
):
    if not authenticate_user(email, password):
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, "error": "Invalid credentials"}
        )
    
    # Create global session
    session_id = await session_store.create_session(email)
    
    if service_url:
        # Generate one-time code
        origin = hashlib.sha256(service_url.encode()).hexdigest()[:10]
        code = create_code(email, origin)
        return RedirectResponse(f"{service_url}?code={code}")
    
    return RedirectResponse("/")