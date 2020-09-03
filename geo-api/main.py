import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


from app import blueprint
from app.src import create_app, db
from app.src.model import polygon, location, matrix_row

flask_app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
flask_app.register_blueprint(blueprint)
flask_app.app_context().push()

manager = Manager(flask_app)
manager.add_command('db', MigrateCommand)

migrate = Migrate(flask_app, db)


@manager.command
def run():
    flask_app.run()


if __name__ == '__main__':
    manager.run()