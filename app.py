from gevent.pywsgi import WSGIServer

from model import app
from schema import (BookingSchema, UserSchema, AuditoriumSchema)
from model import (db, Users, Auditorium, Booking)
from flask import request, jsonify
from flask import abort
from marshmallow import ValidationError
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager, login_user


from flask_httpauth import HTTPBasicAuth


login_manager = LoginManager()
auth = HTTPBasicAuth()
cors = CORS(app)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)
auditorium_schema = AuditoriumSchema()
auditoriums_schema = AuditoriumSchema(many=True)
bcrypt = Bcrypt()

login_manager.login_view = 'auth.login'
login_manager.init_app(app)



@login_manager.user_loader
def load_user(uid):
    return Users.query.get(int(uid))




@auth.verify_password
def verify(name, password):
    user = Users.query.filter_by(name=name).first()
    if user is None:
        abort(401, description="UnauthorizedError")
    if not bcrypt.check_password_hash(user.password, password):
        abort(401, description="UnauthorizedError")
    return True


@app.route('/login', methods=['GET'])
#@auth.login_required()
def user_login():
   return jsonify(message="You are logged in", status=200)



@app.route('/register', methods=['POST'])
def create_user():
    if request.method == 'POST':
        user_data = request.get_json()
        email = user_data.get('email')
        password = user_data.get('password')
        name = user_data.get('name')
        hash_password = bcrypt.generate_password_hash(password)

        try:
            UserSchema().load(user_data)
        except ValidationError:
            abort(400, description="Error validation")

        new_user = Users(email, hash_password, name)

        db.session.add(new_user)
        db.session.commit()

        return jsonify(UserSchema().dump(new_user))


@app.route('/users', methods=['GET'])
def users():
    all_users = Users.query.all()
    if all_users is None:
        abort(404, description="Resource not found")
    result = users_schema.dump(all_users)
    return jsonify(result)


@app.route('/user/<uid>', methods=['GET'])
def get_user(uid):
    if request.method == 'GET':
        user = Users.query.filter_by(uid=uid).first()
        if user is None:
            abort(404, description="Resource not found")
        return UserSchema().dump(user)



@app.route('/user/edit/<uid>', methods=['PUT'])
def update_user(uid):
    if request.method == 'PUT':
        user_data = request.args
        email = user_data.get('email')
        name = user_data.get('name')


        user = Users.query.filter_by(uid=uid).first()
        if user is None:
            abort(404, description="Resource not found")

        try:
            UserSchema().load(user_data)
        except ValidationError:
            abort(400, description="Error validation")

        user.name = name
        user.email = email


        db.session.commit()
        return user_schema.jsonify(user)



@app.route('/user/delete/<uid>', methods=['DELETE'])
def delete_user(uid):
    if request.method == 'DELETE':
        user = Users.query.filter_by(uid=uid).first()
        if user is None:
            abort(404, description="Resource not found")
        db.session.delete(user)
        db.session.commit()

        return jsonify(user_schema.dump({"code": 200}))



@app.route('/auditorium/create', methods=['POST'])
def create_auditorium():
    if request.method == 'POST':
        auditorium_data = request.get_json()
        name = auditorium_data.get('name')
        description = auditorium_data.get('description')
        try:
            AuditoriumSchema().load(auditorium_data)
        except ValidationError:
            abort(400, description="Error validation")

        new_auditorium = Auditorium(name, description)

        db.session.add(new_auditorium)
        db.session.commit()

        return jsonify(AuditoriumSchema().dump(new_auditorium))


@app.route('/auditorium/<int:id>', methods=['GET'])
def get_auditorium_id(id):
    auditorium = Auditorium.query.get(id)
    if auditorium is None:
        abort(404, description="Resource not found")
    return jsonify(AuditoriumSchema().dump(auditorium))



@app.route('/auditorium/edit/<int:ids>', methods=['PUT'])
def update_auditorium(ids):
    if request.method == 'PUT':

        auditorium = Auditorium.query.get(ids)
        if auditorium is None:
            abort(404, description="Resource not found")
        auditorium_data = request.args
        name = auditorium_data.get('name')
        description = auditorium_data.get('description')
        auditorium.name = name
        auditorium.description = description
        db.session.commit()
        return auditorium_schema.jsonify(auditorium)



@app.route('/auditorium/delete/<int:ids>', methods=['DELETE'])
def delete_auditorium(ids):
    if request.method == 'DELETE':
        auditorium = Auditorium.query.get(ids)
        if auditorium is None:
            abort(404, description="Resource not found")

        db.session.delete(auditorium)
        db.session.commit()

        all_auditoriums = Auditorium.query.all()
        result = auditoriums_schema.dump(all_auditoriums)
        return jsonify(result)



@app.route('/auditoriums', methods=['GET'])
def blog():
    if request.method == 'GET':
        all_auditoriums = Auditorium.query.all()
        if all_auditoriums is None:
            abort(404, description="Resource not found")
        result = auditoriums_schema.dump(all_auditoriums)
        return jsonify(result)

@app.route("/booking", methods=["GET","POST"])
def create_booking():
    booking_data = request.json()
    user_uid = booking_data.get('user_uid')
    auditorium_uid = booking_data.get('auditorium_uid')
    booking_date_start = booking_data.get('booking_date_start')
    booking_date_final = booking_data.get('booking_date_final')



    try:
        booking_schema.load(booking_data)
    except ValidationError:
        abort(400, description="Error validation")

    new_booking = Booking(user_uid, auditorium_uid, booking_date_start, booking_date_final)

    db.session.add(new_booking)
    db.session.commit()
    #if(datetime_validation(Booking.auditorium_uid, Booking.booking_date_start, Booking.booking_date_final)==True):
    return jsonify(booking_schema.dump(new_booking))






server = WSGIServer(('127.0.0.1', 5000), app)
server.serve_forever()

