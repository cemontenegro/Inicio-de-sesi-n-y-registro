#from  flask_app.config.mysqlconnection import *

from flask_app.config.mysqlconnection import connectToMySQL
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Usuario:
	db_name="login_registration"

	def __init__( self , data ):
		self.id = data['id']
		self.nombre = data['nombre']
		self.apellido = data['apellido']
		self.email = data['email']
		self.password = data['password']

	@classmethod
	def get_by_email(cls,data):
		query = "SELECT * FROM usuarios WHERE email = %(email)s;"
		result = connectToMySQL(cls.db_name).query_db(query,data)
		if len(result) < 1:
			return False
		return cls(result[0])

	@classmethod
	def save(cls,data):
		query = "INSERT INTO usuarios (nombre,apellido,email, password) VALUES (%(nombre)s,%(apellido)s,%(email)s, %(password)s);"
		return connectToMySQL(cls.db_name).query_db(query, data)

	@classmethod
	def get_by_id(cls,data):
		query = "SELECT * FROM usuarios WHERE id = %(owner_id)s;"
		result = connectToMySQL(cls.db_name).query_db(query,data)
		if len(result) < 1:
			return False
		return cls(result[0])

	@staticmethod
	def is_valid(usuario):
		is_valid = True
		if len(usuario['nombre']) < 2:
			is_valid = False
			flash("Nombre mas de 2 caracteres.")
		if len(usuario['apellido']) < 2:
			is_valid = False
			flash("Apellido mas de 2 caracteres.")
		query = "SELECT * FROM usuarios WHERE email = %(email)s;"
		results = connectToMySQL(Usuario.db_name).query_db(query,usuario)
		if len(results) >= 1:
			flash("Email already taken.")
			is_valid=False
		if not EMAIL_REGEX.match(usuario['email']):
			flash("Email Invalido!!!")
			is_valid=False
		if len(usuario['password']) < 8:
			is_valid = False
			flash("Password mas de 8 caracteres.")
		return is_valid
