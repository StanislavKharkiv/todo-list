import re
import models
import hashlib
from functools import wraps
from flask import request, render_template, redirect, session

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

def routes(app):
    @app.context_processor
    def inject_user():
        user_email = session.get("user")
        return dict(
            is_logged=bool(user_email),
            user_email=user_email,
        )

    @app.route("/")
    @login_required
    def index():
        return render_template("new_task.html")

    @app.route("/tasks", methods=["POST", "GET"])
    @login_required
    def tasks():
        if request.method == "POST":
            form_method = request.args.get("method")
            if form_method == "post":
                models.tasks.add_task(request.form)
                return redirect("/tasks")

            elif form_method == "delete":
                id = request.args.get("id")
                permanently = request.args.get("permanently")
                if permanently:
                    models.tasks.delete_task_permanently(id)
                    return redirect("/tasks/deleted")
                else:
                    models.tasks.delete_task(id)
                    return redirect("/tasks")

            elif form_method == "patch":
                id = request.args.get("id")
                models.tasks.complete_task(id)
                return redirect("/tasks")

        else:
            task_list = models.tasks.get_tasks()
            return render_template("task_list.html", tasks=task_list)

    @app.route("/tasks/deleted")
    @login_required
    def deleted_tasks():
        task_list = models.tasks.get_deleted_tasks()
        return render_template("task_list.html", tasks=task_list, delete=True)

    @app.route("/signup", methods=["POST", "GET"])
    @guest_route
    def signup():
        if request.method == "POST":
            email = request.form["email"].strip()
            password = request.form["password"].strip()
            pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
            if not re.match(pattern, email):
                error = "Wrong email address"
                return render_template(
                    "signup.html", email_error=error, email=email, password=password
                )
            elif len(password) < 8:
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
                return "<h1>You are registered!</h2><a href='/'>Go home</a>"
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
            if len(user) > 0 and user[0][2] == hashed_password.hexdigest():
                session["user"] = user[0][1]
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
