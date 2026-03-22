from flask import Flask
import os


def create_app() -> Flask:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "templates"),
        static_folder=os.path.join(base_dir, "static"),
        static_url_path="/static",
    )
    app.secret_key = os.environ.get("SECRET_KEY", "blackjack-dev-key-change-in-prod")

    from . import routes
    app.register_blueprint(routes.bp)

    return app
