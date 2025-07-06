from fastapi.responses import RedirectResponse
from db import get_db

def check_login(request):
    if not request.cookies.get("user"):
        return RedirectResponse(url="/login", status_code=302)
    return None

def verify_user(username, password):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
    conn.close()
    return user
