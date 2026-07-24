from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from config import DevConfig

# Initialize database instance
db = SQLAlchemy()


def create_app(config_object=None):
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(config_object or DevConfig)

    db.init_app(app)

    from .main import main as main_blueprint
    from .api import api as api_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint, url_prefix="/api")

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("500.html"), 500

    with app.app_context():
        db.create_all()

    return app
