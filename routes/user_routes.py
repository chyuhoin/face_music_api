from flask import Blueprint, jsonify, request, g

user_routes = Blueprint('api_routes', __name__)

@user_routes.route('/user/info/<id>', methods=['GET'])
def info(id):
    cursor = getattr(g, 'db', None).cursor()
    cursor.execute(f"select * from t_user where id = '{id}'")
    info = cursor.fetchone()
    cursor.close()
    return jsonify(info)

@user_routes.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    cursor = getattr(g, 'db', None).cursor()
    cursor.execute(f"select uid from t_user where phone = '{data['phone']}' and password = '{data['password']}'")
    uid = cursor.fetchone()
    if uid is None:
        uid = ["-1"]
    cursor.close()
    print(uid)
    return jsonify(uid[0])

@user_routes.route('/user/register', methods=['POST'])
def register():
    data = request.get_json()
    conn = getattr(g, 'db', None)
    cursor = conn.cursor()
    cursor.execute(f"insert into t_user (uid, phone, password) values ('{data['uid']}', '{data['phone']}', '{data['password']}') RETURNING id")
    id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return jsonify({'id': id})