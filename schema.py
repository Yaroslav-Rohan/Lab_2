from flask_marshmallow import Marshmallow
from marshmallow import validate, fields
from flask_bcrypt import generate_password_hash
from model import app

ma = Marshmallow(app)


class UserSchema(ma.Schema):
    email = fields.String(required=True, validate=validate.Email())
    password = fields.Function(deserialize=lambda obj: generate_password_hash(obj), load_only=True)
    name = fields.String(required=True)


class AuditoriumSchema(ma.Schema):
    name = fields.String(required=True)
    description = fields.String(required=True)


class BookingSchema(ma.Schema):
    user_uid = fields.Integer(attribute="user_uid")
    auditorium_uid = fields.Integer(attribute="auditorium_uid")
    booking_date_start = fields.DateTime(required=True)
    booking_date_final = fields.DateTime(required=True)
