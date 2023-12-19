from flask import Flask
from .models import db
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r'/search/*' : {'origins': '*'}})
app.config.from_object('nutrition_api.app.config.prodConfig')

from .views.searchViews import searchViews
from .views.database.workoutViews import workoutDatabaseViews

app.register_blueprint(searchViews, url_prefix='/search')
app.register_blueprint(workoutDatabaseViews, url_prefix='/database')

db.init_app(app)

migrate = Migrate(app, db, directory='nutrition_api/migrations')
migrate.init_app(app)

with app.app_context():
    db.create_all()




