from functools import wraps
from flask import redirect, session

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = session.get("user")
        if auth: return f(*args, **kwargs)
        return redirect("/login")
    return decorated

def guest_route(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = session.get("user")
        if auth: return redirect("/")
        return f(*args, **kwargs)
    return decorated