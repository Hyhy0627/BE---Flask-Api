from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from app.models.user import User
from marshmallow import fields

class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = auto_field()
    email = auto_field()
    # Password không phải field DB nên dùng riêng
    password = fields.String(load_only=True)
