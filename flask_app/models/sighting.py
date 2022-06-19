from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.skeptics import Skeptic

class Sighting:
    def __init__(self, data):
        self.id = data['id']
        self.reported_by = data['reported_by']
        self.reported_by_name = data['reported_by_name']
        self.date_sighted = data['date_sighted']
        self.location = data['location']
        self.what_happened = data['what_happened']
        self.num_of_sasquatches = data['num_of_sasquatches']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.skeptics = []
        self.skeptic_count = 0

    @classmethod
    def get_all(cls):
        query = f"""
            SELECT sightings.*, CONCAT(users.first_name, ' ', users.last_name) as reported_by_name
            FROM sightings
            JOIN users ON users.id = sightings.reported_by;
        """
        results = cls.run_query(query)

        # if not len(results) > 0:
        #     return False

        items = []
        for row in results:
            item = cls(row)
            item.skeptics = Skeptic.get_by_sighting_id(item.id)
            item.skeptic_count = len(item.skeptics)
            items.append( item )
            
        return items  

    @classmethod
    def get_by_id(cls, id):
        query = f"""
            SELECT sightings.*, CONCAT(users.first_name, ' ', users.last_name) as reported_by_name
            FROM sightings
            JOIN users ON users.id = sightings.reported_by
            WHERE sightings.id=%(id)s;
        """
        data = { "id": id }
        results = cls.run_query(query, data)

        if len(results) > 0:
            item = cls(results[0])
            item.skeptics = Skeptic.get_by_sighting_id(item.id)
        else:
            return False

        return item

    @classmethod
    def save(cls, data ):
        query = f"""
            INSERT INTO sightings ( reported_by, date_sighted, location, what_happened, num_of_sasquatches, created_at, updated_at) 
            VALUES ( %(reported_by)s, %(date_sighted)s, %(location)s, %(what_happened)s, %(num_of_sasquatches)s, NOW(), NOW() );
        """
        return cls.run_query(query, data)

    @classmethod
    def update(cls, data ):
        query = f"""
            UPDATE sightings 
            SET reported_by=%(reported_by)s, 
            date_sighted=%(date_sighted)s , 
            location=%(location)s , 
            what_happened=%(what_happened)s , 
            num_of_sasquatches=%(num_of_sasquatches)s , 
            updated_at=NOW() 
            WHERE id=%(id)s;
        """
        return cls.run_query(query, data)

    @classmethod
    def delete_by_id(cls, id ):
        query = "DELETE FROM sightings WHERE id=%(id)s;"
        data = { "id": id }
        return cls.run_query( query, data )  

    @classmethod
    def run_query(cls, query, data=None):
        return connectToMySQL('sasquatches').query_db( query, data )

    @staticmethod
    def validate_sighting(data):
        is_valid = True
        if not len(data['location']) > 0:
            flash({"label": "location", "message": "Must include a location of sighting"},"sighting")
            is_valid = False
        if not len(data['what_happened']) > 0:
            flash({"label": "what_happened", "message": "Please tell us what happened!!"},"sighting")
            is_valid = False
        if data['date_sighted'] == "":
            flash({"label": "date_sighted", "message": "Must enter a date of sasquatch sighting."},"sighting")
            is_valid = False              
        if data['num_of_sasquatches'] == "" or int(data['num_of_sasquatches']) < 1:
            flash({"label": "num_of_sasquatches", "message": "You must see at least one sasquatch for this to count!"},"sighting")
            is_valid = False

        return is_valid
