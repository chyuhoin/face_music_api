from flask import Flask
from flask_cors import CORS
from utils.database import init_db
from routes.user_routes import user_routes
from routes.photo_routes import photo_routes

app = Flask(__name__)
cors = CORS(app)
init_db(app)

app.config['DATABASE_HOST'] = '159.138.245.76'
app.config['DATABASE_PORT'] = 5432
app.config['DATABASE_NAME'] = 'music'
app.config['DATABASE_USER'] = 'root'
app.config['DATABASE_PASSWORD'] = 'SEU.software@music##'

app.register_blueprint(user_routes)
app.register_blueprint(photo_routes)
