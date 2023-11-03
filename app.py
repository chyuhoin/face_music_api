from flask import Flask
from utils.database import init_db
from routes.user_routes import user_routes

app = Flask(__name__)
init_db(app)

app.config['DATABASE_HOST'] = '159.138.245.76'
app.config['DATABASE_PORT'] = 5432
app.config['DATABASE_NAME'] = 'music'
app.config['DATABASE_USER'] = 'root'
app.config['DATABASE_PASSWORD'] = 'SEU.software@music##'

app.register_blueprint(user_routes)
