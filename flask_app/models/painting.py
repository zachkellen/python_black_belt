from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, request
from flask_app.models.user import User

class Painting():
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.quantity = data['quantity']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
        # self.purchase_amount = 0

    @classmethod
    def create_painting(cls,data):
        query = 'INSERT INTO paintings (title, description, price, quantity, user_id) VALUES (%(title)s, %(description)s, %(price)s, %(quantity)s, %(user_id)s);'
        result = connectToMySQL('final_exam_schema').query_db(query, data)
        return result

    @classmethod
    def get_all_paintings(cls):
        query = "SELECT * FROM paintings JOIN users ON paintings.user_id = users.id;"
        results = connectToMySQL('final_exam_schema').query_db(query)
        paintings = []
        for item in results:
            newPainting = Painting(item)
            user_data = {
                'id': item['users.id'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'email': item['email'],
                'password': item['password'],
                'created_at': item['users.created_at'],
                'updated_at': item['users.updated_at']
            }
            newUser = User(user_data)
            newPainting.user = newUser
            paintings.append(newPainting)
        return paintings

    @classmethod
    def get_painting_by_id(cls, data):
        query = "SELECT * FROM paintings JOIN users ON paintings.user_id = users.id WHERE paintings.id = %(id)s;"
        results = connectToMySQL('final_exam_schema').query_db(query, data)[0]
        newPainting = Painting(results)
        user_data = {
            'id': results['users.id'],
            'first_name': results['first_name'],
            'last_name': results['last_name'],
            'email': results['email'],
            'password': results['password'],
            'created_at': results['users.created_at'],
            'updated_at': results['users.updated_at']
        }
        newUser = User(user_data)
        newPainting.user = newUser
        return newPainting

    @classmethod
    def update_painting(cls,data):
        query = 'UPDATE paintings SET title = %(title)s, description = %(description)s, price = %(price)s, quantity = %(quantity)s WHERE id = %(id)s;'
        result = connectToMySQL('final_exam_schema').query_db(query, data)
        return result

    @classmethod
    def delete_painting(cls,data):
        query = 'DELETE FROM paintings WHERE id = %(id)s;'
        result = connectToMySQL('final_exam_schema').query_db(query, data)

    @classmethod
    def delete_purchase(cls,data):
        query = 'Delete FROM users_has_paintings WHERE painting_id = %(id)s'
        result = connectToMySQL('final_exam_schema').query_db(query, data)

    @classmethod
    def purchase_painting(cls,data):
        query = 'INSERT INTO users_has_paintings (user_id,painting_id) VALUES (%(user_id)s, %(painting_id)s);'
        result = connectToMySQL('final_exam_schema').query_db(query, data)
        return result

    @classmethod
    def get_my_paintings(cls, data):
        query = "SELECT * FROM paintings JOIN users_has_paintings ON paintings.id = users_has_paintings.painting_id JOIN users ON paintings.user_id = users.id WHERE users_has_paintings.user_id = %(id)s;"
        results = connectToMySQL('final_exam_schema').query_db(query, data)
        paintings = []
        for item in results:
            newPainting = Painting(item)
            user_data = {
                'id': item['users.id'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'email': item['email'],
                'password': item['password'],
                'created_at': item['users.created_at'],
                'updated_at': item['users.updated_at']
            }
            newUser = User(user_data)
            newPainting.user = newUser
            paintings.append(newPainting)
        return paintings

    @classmethod
    def get_count(cls,data):
        query = 'SELECT COUNT(paintings.title) FROM paintings JOIN users_has_paintings ON paintings.id = users_has_paintings.painting_id WHERE users_has_paintings.painting_id = %(id)s GROUP BY users_has_paintings.painting_id;'
        print(query)
        results = connectToMySQL('final_exam_schema').query_db(query, data)
        if len(results) == 0:
            return 0
        if len(results) > 0:
            results = connectToMySQL('final_exam_schema').query_db(query, data)[0]
            purchases = results['COUNT(paintings.title)']
            return purchases



    @staticmethod
    def painting_validator(data):
        is_valid = True
        if len(data['title']) < 2 or len(data['title']) > 45:
            flash('Title must be between 2 and 45 characters.')
            is_valid = False
        if len(data['description']) < 10:
            flash('Description must be longer than 10 characters.')
            is_valid = False
        if data['price'] == '':
            flash('Please enter a price.')
            is_valid = False
        if data['price'] != '' and int(data['price']) <= 0:
            flash('Price must be greater than $0.')
            is_valid = False
        if data['quantity'] == '':
            flash('Please enter a quantity.')
            is_valid = False
        if data['quantity'] != '' and int(data['quantity']) <= 0:
            flash('Quantity must be greater than 0.')
            is_valid = False
        
        return is_valid