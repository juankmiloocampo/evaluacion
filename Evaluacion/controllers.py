
from flask.views import MethodView
from flask import jsonify, make_response, request
from model import users
import bcrypt
import jwt
from config import KEY_TOKEN_AUTH
import datetime
from marshmallow import Schema, fields
from marshmallow import validate, ValidationError
from validators import *
import pymysql

create_register_schema = RegisterSchema()
create_login_schema = LoginSchema()
create_productos_schema = ProductosSchema()

class RegisterControllers(MethodView):
  
    def post(self):
        content = request.get_json()
        nombres = content.get("nombres")
        apellidos = content.get("apellidos")
        email = content.get("email")
        password = content.get("password")

        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(bytes(str(password), encoding= 'utf-8'), salt)

        errors = create_register_schema.validate(content)
        if errors:
            return errors, 400

        conn = pymysql.connect(
        host="localhost", port=3306, user="root",
        passwd="Sena1234", db="evaluacion2236347"
        )
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios(nombres,apellidos,email,password) VALUES(%s, %s, %s, %s)",
             (nombres,apellidos,email,hash_password)
        )

        conn.commit()
        conn.close()

        return "Registro OK", 200



class LoginControllers(MethodView):
 
    def post(self):
        content = request.get_json()
        password = bytes(str(content.get("password")), encoding= 'utf-8')
        email = content.get("email")

        errors = create_login_schema.validate(content)
        if errors:
            return errors, 400

        conn = pymysql.connect(
                host="localhost", port=3306, user="root",
                passwd="Sena1234", db="evaluacion2236347"
        )
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT password FROM usuarios WHERE email='{email}'; "
        )
        resultado = cursor.fetchall()
        conn.commit()
        conn.close()

        if len(resultado) > 0:
            if bcrypt.checkpw(password, bytes(resultado[0][0], encoding='utf-8')):
                encoded_jwt = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=300), 'email': email, "password":bytes.decode(password, encoding='utf-8')}, KEY_TOKEN_AUTH , algorithm='HS256')
                return jsonify({"Status": "Login OK", "token": encoded_jwt}), 200
            return jsonify({"Status": "Login incorrecto, contraseña no coincide."}), 400
        return jsonify({"Status": "Login incorrecto, no existe el usuario"}), 400

class CrearControllers(MethodView):
    
    def post(self):
        content = request.get_json()
        nombre = content.get("nombre")
        precio = content.get("precio")

        errors = create_productos_schema.validate(content)
        if errors:
            return errors, 400

        if(request.headers.get('Authorization')):
            token = request.headers.get('Authorization').split(" ")
            try:
                data = jwt.decode(token[1], KEY_TOKEN_AUTH , algorithms=['HS256'])
                conn = pymysql.connect(
                host="localhost", port=3306, user="root",
                passwd="Sena1234", db="evaluacion2236347"
                )
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO productos(nombre, precio) VALUES(%s, %s)",
                    (nombre, precio)
                )
                conn.commit()
                conn.close()
                return jsonify({"Status": "Autorizado por token", "Producto registrado": nombre}), 200
            except:
                return jsonify({"Status": "TOKEN NO VALIDO"}), 403
        return jsonify({"Status": "No ha enviado un token"}), 403


class ProductosControllers(MethodView):
    
    def get(self):
        conn = pymysql.connect(
                host="localhost", port=3306, user="root",
                passwd="Sena1234", db="evaluacion2236347"
        )
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT * FROM productos;"
        )
        resultado = cursor.fetchall()
        conn.commit()
        conn.close()
        total_productos = {}
        for producto in resultado:
            total_productos[producto[0]] = {
                "Precio":producto[2],
                "Producto":producto[1]
            }
            
        return make_response(jsonify({
            "Productos": total_productos
        }), 200)
