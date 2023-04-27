from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user_model import User
import re
from flask import flash

price_regex = re.compile(r"^[0-9]*$")

class ActionFigure:
    db = "figures_mod"
    def __init__(self,data):
        self.id = data['id']
        self.figure_name = data['figure_name']
        self.brand = data['brand']
        self.line = data['line']
        self.price = data['price']
        self.description = data['description']
        self.image = data['image']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    
    @classmethod
    def get_specific_figure(cls,data):
        query = "SELECT * FROM figures_table LEFT JOIN users ON figures_table.user_id = users.id WHERE figures_table.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print (results)
        figure = cls( results[0])
        for row in results:
            user_data = {
                "id": row['id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at":row['created_at'],
                "updated_at":row['updated_at']
            }
            figure.user = User(user_data)
        return figure
    

    @classmethod
    def save(cls,data):
        query = "INSERT INTO figures_table (figure_name, brand, line, price, description, image, user_id) VALUES(%(figure_name)s,%(brand)s,%(line)s,%(price)s, %(description)s,%(image)s,%(user_id)s)"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM figures_table;"
        results = connectToMySQL(cls.db).query_db(query)
        figure = []
        for row in results:
            figure.append( cls(row))
        return figure
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM figures_table WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print (results)
        return cls( results[0])
    
    
    @classmethod
    def update(cls,data):
        query = """UPDATE figures_table
        SET figure_name=%(figure_name)s, brand=%(brand)s, line=%(line)s,price=%(price)s, description=%(description)s, image=%(image)s, updated_at=NOW()
        WHERE id=%(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM figures_table WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_figure(figures_table):
        is_valid = True
        print(figures_table)
        if len(figures_table['figure_name']) < 2:
            is_valid = False
            flash("Name must be at least 2 characters","show")
        if len(figures_table['brand']) < 2:
            is_valid = False
            flash("Name must be at least 2 characters","show")
        if len(figures_table['line']) < 2:
            is_valid = False
            flash("Name must be at least 2 characters","show")
        if len(figures_table['price']) < 1:
            is_valid = False
            flash("Price must be greater than 0","show")
        if not price_regex.match(figures_table['price']):
            flash("Price must be filled out","show")
            is_valid = False
        if len(figures_table['description']) < 10:
            is_valid = False
            flash("Description must be at least 10 characters","show")
        return is_valid