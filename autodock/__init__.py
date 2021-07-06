from flask import Flask
from autodock.config import Config


def create_app(conf=Config):
    app = Flask(__name__)
    app.config.from_object(conf)
    from autodock.VINA.routes import mainapp
    app.register_blueprint(mainapp)
    return app
