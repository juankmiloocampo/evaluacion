from marshmallow import Schema, fields
from marshmallow import validate, ValidationError


class RegisterSchema(Schema):
    nombres = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    apellidos = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    password = fields.Str(required=  True, validate=validate.Length(min=8, max=12))
    email = fields.Str(required=True, validate=validate.Email())

class LoginSchema(Schema):
    password = fields.Str(required=  True, validate=validate.Length(min=8, max=12))
    email = fields.Str(required=True, validate=validate.Email())
    
class ProductosSchema(Schema):
    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    precio = fields.Int(required=True, validate=validate.Range(min=1, max=1000000))
