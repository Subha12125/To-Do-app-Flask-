from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import click
import os

# Create database object globally
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'your_secret_key_here_change_in_production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Link db object to the app
    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    # Add CLI commands for database management
    @app.cli.command()
    def init_db():
        """Initialize the database."""
        db.create_all()
        click.echo('Database initialized successfully!')

    @app.cli.command()
    def reset_db():
        """Reset the database."""
        db.drop_all()
        db.create_all()
        click.echo('Database reset successfully!')

    return app