from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Skeptic:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.sighting_id = data['sighting_id']
        self.skeptic_name = data['skeptic_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at'] 

    @classmethod
    def get_by_sighting_id(cls, id):
        query = f"""
            SELECT skeptics.*, CONCAT(users.first_name, ' ', users.last_name) as skeptic_name
            FROM skeptics
            JOIN users ON users.id = skeptics.user_id
            WHERE skeptics.sighting_id=%(id)s;
        """
        data = { "id": id }
        results = cls.run_query(query, data)
        print(results)

        items = []
        for row in results:
            items.append( cls(row) )

        return items

    @classmethod
    def save(cls, data ):
        query = f"""
            INSERT INTO skeptics ( user_id, sighting_id, created_at, updated_at) 
            VALUES ( %(user_id)s, %(sighting_id)s, NOW(), NOW() );
        """
        return cls.run_query(query, data)

    @classmethod
    def delete(cls, data ):
        query = "DELETE FROM skeptics WHERE user_id=%(user_id)s and sighting_id=%(sighting_id)s;"
        return cls.run_query( query, data )  

    @classmethod
    def run_query(cls, query, data=None):
        return connectToMySQL('sasquatches').query_db( query, data )