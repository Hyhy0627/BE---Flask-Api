from marshmallow import Schema, fields

class UserSchema(Schema):
    """Schema for serializing/deserializing user objects"""
    
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    password = fields.String(load_only=True)
    role = fields.String(dump_only=True)  # Role is read-only in responses