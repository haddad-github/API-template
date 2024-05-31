from flask_sqlalchemy import SQLAlchemy

#Initialize SQLAlchemy with Flask app
database = SQLAlchemy()

#Define the models (a Class represents a Table in the database)
class Movie(database.Model):
    """
    Class represents the table Movie and its columns
    """
    #Table name (should match actual name, otherwise generates a name based on the class name)
    __tablename__ = 'movies'

    #Columns
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    poster_link = database.Column(database.String, nullable=True, name='poster_link')
    series_title = database.Column(database.String, nullable=False, name='series_title')
    released_year = database.Column(database.Integer, nullable=True, name='released_year')
    certificate = database.Column(database.String, nullable=True, name='certificate')
    runtime = database.Column(database.String, nullable=True, name='runtime')
    genre = database.Column(database.String, nullable=True, name='genre')
    imdb_rating = database.Column(database.Float, nullable=True, name='imdb_rating')
    overview = database.Column(database.String, nullable=True, name='overview')
    meta_score = database.Column(database.Integer, nullable=True, name='meta_score')
    director = database.Column(database.String, nullable=True, name='director')
    star1 = database.Column(database.String, nullable=True, name='star1')
    star2 = database.Column(database.String, nullable=True, name='star2')
    star3 = database.Column(database.String, nullable=True, name='star3')
    star4 = database.Column(database.String, nullable=True, name='star4')
    no_of_votes = database.Column(database.Integer, nullable=True, name='no_of_votes')
    gross = database.Column(database.String, nullable=True, name='gross')

    #Convert to dictionary for JSON serialization
    def to_dict(self):
        data = {}
        #Iterate through each column in the table
        for column in self.__table__.columns:
            #Retrieve the attribute value
            value = getattr(self, column.name)
            data[column.name] = value
        return data