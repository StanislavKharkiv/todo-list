import models
from flask import request, render_template, redirect


def routes(app):
    @app.route("/")
    def index():
        return render_template("new_task.html")

    @app.route("/tasks", methods=["POST", "GET"])
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
    def deleted_tasks():
        task_list = models.tasks.get_deleted_tasks()
        return render_template("task_list.html", tasks=task_list, delete=True)
