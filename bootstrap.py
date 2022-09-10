from flask import Flask

import settings
from gnchat.orm import init_db
from gnchat.main.blueprint import main_blueprint
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = settings.SQLALCHEMY_COMMIT_ON_TEARDOWN
app.config['CORS_ALLOW_HEADERS'] = 'Content-Type'
app.config['CORS_ALLOW_METHODS'] = 'GET,POST,OPTIONS'
CORS(app, supports_credentials=False, resources={r"/*": {"origins": "*"}})

app.register_blueprint(main_blueprint)
init_db(app)

if __name__ == '__main__':
    app.run()
