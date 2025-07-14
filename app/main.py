from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import auth, pr, dashboard, user

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(auth.router)
app.include_router(pr.router)
app.include_router(dashboard.router)
app.include_router(user.router)

# Optionally, add a root redirect
from fastapi.responses import RedirectResponse
@app.get("/")
def root():
    return RedirectResponse(url="/dashboard")
