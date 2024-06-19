import models
from flask import request, render_template, redirect, session
from .wraps import login_required


def tasks(app):
    @app.route("/")
    @login_required
    def index():
        return render_template("new_task.html")

    @app.route("/tasks", methods=["POST", "GET"])
    @login_required
    def tasks():
        user = session.get("user")
        if request.method == "POST":
            form_method = request.args.get("method")
            if form_method == "post":
                models.tasks.add_task(request.form, user["id"])
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
            task_list = models.tasks.get_tasks(user["id"])
            return render_template("task_list.html", tasks=task_list)

    @app.route("/tasks/deleted")
    @login_required
    def deleted_tasks():
        user = session.get("user")
        task_list = models.tasks.get_deleted_tasks(user["id"])
        return render_template("task_list.html", tasks=task_list, delete=True)
