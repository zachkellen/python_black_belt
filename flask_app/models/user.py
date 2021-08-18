from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, request
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

class User():
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def register_user(cls,data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        results = connectToMySQL('final_exam_schema').query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL('final_exam_schema').query_db(query,data)
        users = []
        for result in results:
            users.append(User(result))
        return users

    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name']) < 2 or len(data['first_name']) > 45:
            is_valid = False
            flash('First name should be between 2 and 45 characters long.')

        if len(data['last_name']) < 2 or len(data['last_name']) > 45:
            is_valid = False
            flash('Last name should be between 2 and 45 characters long.')

        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address.")
            is_valid = False

        if len(User.get_by_email(request.form)) > 0:
            flash("An account is already linked to this email, please use a different email.")
            is_valid = False

        if len(data['password']) < 8:
            flash("Password needs to be longer than 8 characters")
            is_valid = False

        if re.search('[0-9]', data['password']) is None:
            flash('Your password needs to have a number in it')
            is_valid = False

        if re.search('[A-Z]', data['password']) is None:
            flash("Your password needs to have an uppercase letter in it")
            is_valid = False
        
        if data['password'] != data['confirm_password']:
            flash('Passwords do not match.')
            is_valid = False

        return is_valid

