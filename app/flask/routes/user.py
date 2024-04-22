import re
import hashlib
import models
import settings
from flask import request, render_template, redirect, session
from .wraps import guest_route


def user(app):

    @app.route("/signup", methods=["POST", "GET"])
    @guest_route
    def signup():
        if request.method == "POST":
            email = request.form["email"].strip()
            password = request.form["password"]
            if not re.match(settings.EMAIL_PATTERN, email):
                error = "Wrong email address"
                return render_template(
                    "signup.html", email_error=error, email=email, password=password
                )
            elif len(password) < settings.PASSWORD_MIN_LENGTH:
                error = "Password is too simple"
                return render_template(
                    "signup.html", password_error=error, email=email, password=password
                )
            else:
                db_user = models.users.find_by_email(email)
                if db_user:
                    error = "User with this email already exists"
                    return render_template(
                        "signup.html", email_error=error, email=email, password=password
                    )
                hashed_password = hashlib.sha256(password.encode())
                models.users.signup(
                    {"email": email, "password": hashed_password.hexdigest()}
                )
                return "<h1>You are registered!</h2><a href='/'>Go login</a>"
        else:
            return render_template("signup.html")

    @app.route("/login", methods=["POST", "GET"])
    @guest_route
    def login():
        if request.method == "POST":
            email = request.form["email"].strip()
            password = request.form["password"].strip()
            hashed_password = hashlib.sha256(password.encode())
            user = models.users.find_by_email(email)
            if len(user) > 0 and user[0]['password'] == hashed_password.hexdigest():
                session["user"] = user[0]
                return redirect("/")
            else:
                err = "Wrong email or password!"
                return render_template(
                    "login.html", email=email, password=password, error=err
                )
        else:
            return render_template("login.html")

    @app.route("/logout", methods=["POST", "GET"])
    def logout():
        session.pop("user", None)
        return redirect("/login")
