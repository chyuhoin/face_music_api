import psycopg2
from flask import g

def init_db(app):
    # 在应用上下文中创建数据库连接
    @app.before_request
    def before_request():
        g.db = psycopg2.connect(
        host=app.config['DATABASE_HOST'],
        port=app.config['DATABASE_PORT'],
        dbname=app.config['DATABASE_NAME'],
        user=app.config['DATABASE_USER'],
        password=app.config['DATABASE_PASSWORD']
    )

    # 在应用上下文中关闭数据库连接
    @app.teardown_appcontext
    def teardown_appcontext(error):
        db = getattr(g, 'db', None)
        if db is not None:
            db.close()