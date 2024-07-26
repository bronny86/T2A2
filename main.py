import os

from flask import Flask

from init import db, ma, bcrypt, jwt

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://library_dev:123456@localhost:5432/library_db"

    app.config["JWT_SECRET_KEY"] = "secret"

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from controllers.cli_controller import db_commands
    app.register_blueprint(db_commands)

    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from controllers.playlist_controller import playlists_bp
    app.register_blueprint(playlists_bp)

    from controllers.song_controller import songs_bp
    app.register_blueprint(songs_bp)

    return app