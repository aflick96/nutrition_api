from flask import Flask
from .models import db
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r'/search/*' : {'origins': '*'}})
app.config.from_object('nutrition_api.app.config.prodConfig')


from .views.searchViews import searchViews
app.register_blueprint(searchViews, url_prefix='/search')

db.init_app(app)

migrate = Migrate(app, db)
migrate.init_app(app)

with app.app_context():
    db.create_all()




