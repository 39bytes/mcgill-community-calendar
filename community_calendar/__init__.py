from flask import Flask, send_from_directory
import os
from jinja2 import environment
from flaskext.markdown import Markdown

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    Markdown(app)
    app.config.from_mapping(
        DATABASE = os.path.join(app.instance_path, 'codejam.sqlite'),
        UPLOAD_FOLDER = os.path.join(app.instance_path, 'uploads'),
        SECRET_KEY="dev"
    )

    try:
        os.makedirs(app.instance_path)
        os.makedirs(app.config['UPLOAD_FOLDER'])
    except OSError:
        pass
    

    with app.app_context():
        from . import database
    database.init_db()
    database.init_app(app)

    
    from . import auth
    app.register_blueprint(auth.bp)

    from . import event
    app.register_blueprint(event.bp)

    from . import user
    app.register_blueprint(user.bp)

    @app.route('/uploads/<filename>')
    def send_uploaded_file(filename=''):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    app.add_url_rule('/', 'index')

    return app
