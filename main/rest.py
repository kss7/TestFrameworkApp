from functools import wraps
from flask import jsonify, request, Blueprint, current_app
from flask_accept import accept
import json, jwt, logging
from datetime import datetime, timedelta
from flask_login import login_user, current_user, login_required, logout_user
from main.models import User, UserSchema
from main import db
blueprint = Blueprint('users', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

logging.basicConfig(level=logging.DEBUG)


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user1 = User.query.filter_by(id=data['id']).first()
        except Exception as e:
            return jsonify({
                'message': 'Token is invalid !!',
                "error": str(e)
            }), 500
        # returns the current logged in users contex to the routes
        return f(current_user1, *args, **kwargs)

    return decorated



############## routes #################
@blueprint.route('/', methods=['GET', 'POST'])
def index():
    #if 'email' in session:
    #    username = session['email']
    #   return jsonify({'message': 'You are already logged in', 'username': username})
    #else:
        resp = jsonify({'message': 'Unauthorized access, please login'})
        resp.status_code = 401
        return resp


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    info = json.loads(request.data)
    email = info.get('email')
    password = info.get('password')
    user = User(email, password)
    user_email = User.query.filter_by(email=email).first()
    if user_email:
        return jsonify({"status": 422,
                 "msg": "Username or Password Exists"}), 422
    else:
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return jsonify(user.to_json()), 201


@blueprint.route('/login', methods=['POST'])
def login():
        password = request.json['password']
        email = request.json['email']
        user = User.query.filter_by(email=email).first()
        if user and user.is_correct_password(password):
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            token = jwt.encode(
                {'id': user.get_id(), 'exp': datetime.utcnow() + timedelta(minutes=15)},
                current_app.config['SECRET_KEY'], algorithm="HS256")
            current_app.logger.info('request TOKEN')
            return jsonify({"status": 200, "msg": user.email + " logged in", "userId": str(user.id),
                            'token': token})
        else:
            return jsonify({"status": 401,
                            "reason": "Username or Password does-not exists"}), 401


@blueprint.route("/authuserscount", methods=["GET"])
def get_auth_users():
    auth_users = User.get_auth_user_count()
    return jsonify({"count": auth_users})


@blueprint.route("/users", methods=["GET"])
@token_required
def get_all_users(current_user):
    uid = request.args.get('id')
    if (uid):
        user = User.query.filter_by(id=uid).first()
        return jsonify(user.to_json()), 200
    else:
        result = users_schema.dump(User.get_all_users())
        return jsonify({"users":result}), 200


@blueprint.route('/user/<int:uid>', methods=["GET"])
@token_required
def get_user_withId(current_user, uid: int):
    user = User.query.filter_by(id=uid).first()
    if user:
        return jsonify(user.to_json()), 200
    else:
        return jsonify({"status": 404,
                        "reason": "UserID does-not exists"}), 404

@blueprint.route("/allusercount", methods=["GET"])
@accept('application/json', 'text/html')
def get_all_users_count():
    allusers = User.get_all_users_count()
    #print (allusers)
    return jsonify({'status':{"message": "success", 'status':200}, "count": allusers})


@blueprint.route("/checkusers", methods=["GET"])
def check_total_employee(auth=None, all=None):
    auth_count = auth or User.get_auth_user_count()
    all_count = all or User.get_all_users_count()
    if auth_count > 100:
        return jsonify({"auth_count": auth_count, "all_count":all_count,
                            "msg": "Error! Auth emp count is more than employees"})
    elif auth_count < all_count:
        percent = int((auth_count/all_count)*100)
        if percent < 95:
            return jsonify({"auth_count": auth_count, "all_count":all_count,
                            "msg": "Percentage of joining is too less"})
        else:
            return jsonify({"auth_count": auth_count, "all_count": all_count,
                            "msg": "Percentage of joining is OK"})
    else:
        return jsonify({"auth_count": auth_count, "all_count": all_count,
                            "msg": "All good"})


@blueprint.route('/logout')
def logout():
    pass
    #user = current_user
    #user.authenticated = False
    #logout_user()


@blueprint.route('/delete', methods=['DELETE'])
@token_required
def delete_record(current_user):
    record = json.loads(request.data)
    uid = record.get('id')
    user = User.query.filter_by(id=uid).first()
    if not user:
        return jsonify({'error': 'data not found'}), 404
    else:
        db.session.delete(user)
        db.session.commit()
        return jsonify(user.to_json()), 200