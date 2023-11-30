from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
cors = CORS(app)

# 配置数据库连接信息
app.config['SQLALCHEMY_DATABASE_URI'] = '不告诉你'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的跟踪，以提高性能
app.config['SQLALCHEMY_ECHO'] = True  # 是否回显SQL，部署的时候要关

# 配置JWT密钥
app.config['JWT_SECRET_KEY'] = '不告诉你'

app.config['PROPAGATE_EXCEPTIONS'] = True

db = SQLAlchemy(app)
jwt = JWTManager(app)
