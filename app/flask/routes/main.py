from flask import session
from .tasks import tasks
from .user import user


def routes(app):
    @app.context_processor
    def inject_user():
        user = session.get("user")
        return dict(
            is_logged=bool(user),
            user_email=user['email'] if user else '',
        )

    tasks(app)
    user(app)
