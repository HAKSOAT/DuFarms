from app import app, models
import config
import sqlalchemy as sa


def set_up():
    app.config.from_object(config.DevConfig)
    with app.app_context():
        models.db.init_app(app)
        models.db.create_all()
        # Initialize the database with the location Abroad
        try:
            location = models.Location(name="Abroad", description="Not a warehouse")
            models.db.session.add(location)
            models.db.session.commit()
        except sa.exc.IntegrityError:
            pass
    app.run()


if __name__ == "__main__":
    set_up()
