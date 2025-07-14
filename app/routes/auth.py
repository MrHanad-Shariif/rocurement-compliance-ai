from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.auth import verify_user, create_user, set_reset_token, verify_reset_token, reset_password

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    user = verify_user(username, password)
    if user:
        response = RedirectResponse(url="/dashboard", status_code=302)
        response.set_cookie("user", username)
        return response
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("user")
    return response

@router.get("/signup", response_class=HTMLResponse)
async def signup_get(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup", response_class=HTMLResponse)
async def signup_post(request: Request, username: str = Form(...), password: str = Form(...)):
    if create_user(username, password):
        return RedirectResponse(url="/login", status_code=302)
    else:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Username already exists"})

@router.get("/forgot_password", response_class=HTMLResponse)
async def forgot_password_get(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request})

@router.post("/forgot_password", response_class=HTMLResponse)
async def forgot_password_post(request: Request, username: str = Form(...)):
    token = set_reset_token(username)
    reset_link = f"/reset_password?token={token}"
    return templates.TemplateResponse("forgot_password.html", {"request": request, "reset_link": reset_link})

@router.get("/reset_password", response_class=HTMLResponse)
async def reset_password_get(request: Request, token: str = ""):
    return templates.TemplateResponse("reset_password.html", {"request": request, "token": token})

@router.post("/reset_password", response_class=HTMLResponse)
async def reset_password_post(request: Request, token: str = Form(...), password: str = Form(...)):
    user = verify_reset_token(token)
    if user:
        reset_password(token, password)
        return RedirectResponse(url="/login", status_code=302)
    else:
        return templates.TemplateResponse("reset_password.html", {"request": request, "token": token, "error": "Invalid or expired token"}) 