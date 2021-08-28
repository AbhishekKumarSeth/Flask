# project/server/__init__.py

import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

app = Flask(__name__)
ma = Marshmallow(app)

CORS(app)

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)


migrate = Migrate()
migrate.init_app(app, db)


from project.server.auth.views import auth_blueprint
from project.server.student.views import stu_blueprint
from project.server.azure_blob.upload import azure_blueprint
from project.server.category.views import category_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(stu_blueprint)
app.register_blueprint(azure_blueprint)
app.register_blueprint(category_blueprint)
