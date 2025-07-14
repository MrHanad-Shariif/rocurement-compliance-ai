from fastapi.responses import RedirectResponse
from app.db import get_db
from passlib.hash import bcrypt
import psycopg2.extras
from datetime import datetime, timedelta
import secrets

def check_login(request, required_role=None):
    username = request.cookies.get("user")
    if not username:
        return RedirectResponse(url="/login", status_code=302)
    if required_role:
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT role FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if not user or user["role"] != required_role:
            return RedirectResponse(url="/login", status_code=302)
    return None

def verify_user(username, password):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user and bcrypt.verify(password, user["password"]):
        return user
    return None

def create_user(username, password, role="user"):
    conn = get_db()
    cur = conn.cursor()
    hashed = bcrypt.hash(password)
    try:
        cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, hashed, role))
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

def set_reset_token(username):
    token = secrets.token_urlsafe(32)
    expiry = datetime.utcnow() + timedelta(hours=1)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET reset_token=%s, reset_token_expiry=%s WHERE username=%s", (token, expiry, username))
    conn.commit()
    cur.close()
    conn.close()
    return token

def verify_reset_token(token):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM users WHERE reset_token=%s AND reset_token_expiry > NOW()", (token,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def reset_password(token, new_password):
    hashed = bcrypt.hash(new_password)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET password=%s, reset_token=NULL, reset_token_expiry=NULL WHERE reset_token=%s", (hashed, token))
    conn.commit()
    cur.close()
    conn.close()
