import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from database_models import database, Movie
from dotenv import load_dotenv

#Load environment variables from .env file
load_dotenv()

#Initialize Flask app
app = Flask(__name__)
CORS(app)

#Database configuration
DATABASE = {
    'source': os.getenv('SOURCE', 'postgresql'),
    'username': os.getenv('USERNAME', 'postgres'),
    'password': os.getenv('PASSWORD', '123'),
    'host': os.getenv('DB_HOSTNAME', 'localhost'),
    'port': os.getenv('PORT', '5432'),
    'database_name': os.getenv('DATABASE_NAME', 'movies_db')
}

#Connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = f"{DATABASE['source']}://{DATABASE['username']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['database_name']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Bind the SQLAlchemy instance to the Flask app
database.init_app(app)

#Create the database tables based on your models
with app.app_context():
    database.create_all()

### ROUTES ###
@app.route('/')
def index():
    return "Welcome to the Movie API!"

@app.route('/movies', methods=['GET'])
def get_movies():
    """
    Retrieve all movies
    ---
    tags:
        - Full dump
    responses:
        200:
          description: A list of movies in JSON format.
          schema:
            type: array
            items:
                type: object
                properties:
                    id:
                        type: integer
                    poster_link:
                        type: string
                    series_title:
                        type: string
                    released_year:
                        type: integer
                    certificate:
                        type: string
                    runtime:
                        type: string
                    genre:
                        type: string
                    imdb_rating:
                        type: float
                    overview:
                        type: string
                    meta_score:
                        type: integer
                    director:
                        type: string
                    star1:
                        type: string
                    star2:
                        type: string
                    star3:
                        type: string
                    star4:
                        type: string
                    no_of_votes:
                        type: integer
                    gross:
                        type: string
                example:
                      {
                        "id": 1,
                        "poster_link": "https://example.com/poster.jpg",
                        "series_title": "The Shawshank Redemption",
                        "released_year": 1994,
                        "certificate": "A",
                        "runtime": "142 min",
                        "genre": "Drama",
                        "imdb_rating": 9.3,
                        "overview": "Two imprisoned men bond over a number of years...",
                        "meta_score": 80,
                        "director": "Frank Darabont",
                        "star1": "Tim Robbins",
                        "star2": "Morgan Freeman",
                        "star3": "Bob Gunton",
                        "star4": "William Sadler",
                        "no_of_votes": 2343110,
                        "gross": "28,341,469"
                      }
    """
    movies = Movie.query.all()
    return jsonify([movie.to_dict() for movie in movies]), 200

@app.route('/movies/<int:id>', methods=['GET'])
def get_movie(id):
    """
    Retrieve a movie by ID
    ---
    tags:
        - Single entry
    parameters:
        - name: id
          in: path
          type: integer
          required: true
          description: ID of the movie to retrieve
    responses:
        200:
          description: A movie in JSON format.
          schema:
            type: object
            properties:
                id:
                    type: integer
                poster_link:
                    type: string
                series_title:
                    type: string
                released_year:
                    type: integer
                certificate:
                    type: string
                runtime:
                    type: string
                genre:
                    type: string
                imdb_rating:
                    type: float
                overview:
                    type: string
                meta_score:
                    type: integer
                director:
                    type: string
                star1:
                    type: string
                star2:
                    type: string
                star3:
                    type: string
                star4:
                    type: string
                no_of_votes:
                    type: integer
                gross:
                    type: string
            example:
                  {
                    "id": 1,
                    "poster_link": "https://example.com/poster.jpg",
                    "series_title": "The Shawshank Redemption",
                    "released_year": 1994,
                    "certificate": "A",
                    "runtime": "142 min",
                    "genre": "Drama",
                    "imdb_rating": 9.3,
                    "overview": "Two imprisoned men bond over a number of years...",
                    "meta_score": 80,
                    "director": "Frank Darabont",
                    "star1": "Tim Robbins",
                    "star2": "Morgan Freeman",
                    "star3": "Bob Gunton",
                    "star4": "William Sadler",
                    "no_of_votes": 2343110,
                    "gross": "28,341,469"
                  }
    """
    movie = Movie.query.get(id)
    if movie is None:
        return jsonify({'error': 'Movie not found'}), 404
    return jsonify(movie.to_dict()), 200

@app.route('/movies', methods=['POST'])
def add_movie():
    """
    Add a new movie
    ---
    tags:
        - Create entry
    parameters:
        - in: body
          name: body
          schema:
            type: object
            properties:
                poster_link:
                    type: string
                series_title:
                    type: string
                released_year:
                    type: integer
                certificate:
                    type: string
                runtime:
                    type: string
                genre:
                    type: string
                imdb_rating:
                    type: float
                overview:
                    type: string
                meta_score:
                    type: integer
                director:
                    type: string
                star1:
                    type: string
                star2:
                    type: string
                star3:
                    type: string
                star4:
                    type: string
                no_of_votes:
                    type: integer
                gross:
                    type: string
            required:
                - series_title
                - imdb_rating
            example:
                  {
                    "poster_link": "https://example.com/poster.jpg",
                    "series_title": "New Movie",
                    "released_year": 2021,
                    "certificate": "A",
                    "runtime": "120 min",
                    "genre": "Drama",
                    "imdb_rating": 8.5,
                    "overview": "A new movie overview...",
                    "meta_score": 75,
                    "director": "Some Director",
                    "star1": "Actor One",
                    "star2": "Actor Two",
                    "star3": "Actor Three",
                    "star4": "Actor Four",
                    "no_of_votes": 123456,
                    "gross": "10,000,000"
                  }
    responses:
        201:
          description: The created movie.
          schema:
            type: object
            properties:
                id:
                    type: integer
                poster_link:
                    type: string
                series_title:
                    type: string
                released_year:
                    type: integer
                certificate:
                    type: string
                runtime:
                    type: string
                genre:
                    type: string
                imdb_rating:
                    type: float
                overview:
                    type: string
                meta_score:
                    type: integer
                director:
                    type: string
                star1:
                    type: string
                star2:
                    type: string
                star3:
                    type: string
                star4:
                    type: string
                no_of_votes:
                    type: integer
                gross:
                    type: string
            example:
                  {
                    "id": 101,
                    "poster_link": "https://example.com/poster.jpg",
                    "series_title": "New Movie",
                    "released_year": 2021,
                    "certificate": "A",
                    "runtime": "120 min",
                    "genre": "Drama",
                    "imdb_rating": 8.5,
                    "overview": "A new movie overview...",
                    "meta_score": 75,
                    "director": "Some Director",
                    "star1": "Actor One",
                    "star2": "Actor Two",
                    "star3": "Actor Three",
                    "star4": "Actor Four",
                    "no_of_votes": 123456,
                    "gross": "10,000,000"
                  }
    """
    data = request.get_json()
    new_movie = Movie(
        poster_link=data.get('poster_link'),
        series_title=data.get('series_title'),
        released_year=data.get('released_year'),
        certificate=data.get('certificate'),
        runtime=data.get('runtime'),
        genre=data.get('genre'),
        imdb_rating=data.get('imdb_rating'),
        overview=data.get('overview'),
        meta_score=data.get('meta_score'),
        director=data.get('director'),
        star1=data.get('star1'),
        star2=data.get('star2'),
        star3=data.get('star3'),
        star4=data.get('star4'),
        no_of_votes=data.get('no_of_votes'),
        gross=data.get('gross')
    )
    database.session.add(new_movie)
    database.session.commit()
    return jsonify(new_movie.to_dict()), 201

@app.route('/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    """
    Update a movie by ID
    ---
    tags:
        - Update entry
    parameters:
        - name: id
          in: path
          type: integer
          required: true
          description: ID of the movie to update
        - in: body
          name: body
          schema:
            type: object
            properties:
                poster_link:
                    type: string
                series_title:
                    type: string
                released_year:
                    type: integer
                certificate:
                    type: string
                runtime:
                    type: string
                genre:
                    type: string
                imdb_rating:
                    type: float
                overview:
                    type: string
                meta_score:
                    type: integer
                director:
                    type: string
                star1:
                    type: string
                star2:
                    type: string
                star3:
                    type: string
                star4:
                    type: string
                no_of_votes:
                    type: integer
                gross:
                    type: string
            example:
                  {
                    "poster_link": "https://example.com/poster.jpg",
                    "series_title": "Updated Movie",
                    "released_year": 2021,
                    "certificate": "A",
                    "runtime": "120 min",
                    "genre": "Drama",
                    "imdb_rating": 8.5,
                    "overview": "An updated movie overview...",
                    "meta_score": 75,
                    "director": "Updated Director",
                    "star1": "Updated Actor One",
                    "star2": "Updated Actor Two",
                    "star3": "Updated Actor Three",
                    "star4": "Updated Actor Four",
                    "no_of_votes": 123456,
                    "gross": "10,000,000"
                  }
    responses:
        200:
          description: The updated movie.
          schema:
            type: object
            properties:
                id:
                    type: integer
                poster_link:
                    type: string
                series_title:
                    type: string
                released_year:
                    type: integer
                certificate:
                    type: string
                runtime:
                    type: string
                genre:
                    type: string
                imdb_rating:
                    type: float
                overview:
                    type: string
                meta_score:
                    type: integer
                director:
                    type: string
                star1:
                    type: string
                star2:
                    type: string
                star3:
                    type: string
                star4:
                    type: string
                no_of_votes:
                    type: integer
                gross:
                    type: string
            example:
                  {
                    "id": 101,
                    "poster_link": "https://example.com/poster.jpg",
                    "series_title": "Updated Movie",
                    "released_year": 2021,
                    "certificate": "A",
                    "runtime": "120 min",
                    "genre": "Drama",
                    "imdb_rating": 8.5,
                    "overview": "An updated movie overview...",
                    "meta_score": 75,
                    "director": "Updated Director",
                    "star1": "Updated Actor One",
                    "star2": "Updated Actor Two",
                    "star3": "Updated Actor Three",
                    "star4": "Updated Actor Four",
                    "no_of_votes": 123456,
                    "gross": "10,000,000"
                  }
    """
    data = request.get_json()
    movie = Movie.query.get(id)
    if movie is None:
        return jsonify({'error': 'Movie not found'}), 404

    movie.poster_link = data.get('poster_link', movie.poster_link)
    movie.series_title = data.get('series_title', movie.series_title)
    movie.released_year = data.get('released_year', movie.released_year)
    movie.certificate = data.get('certificate', movie.certificate)
    movie.runtime = data.get('runtime', movie.runtime)
    movie.genre = data.get('genre', movie.genre)
    movie.imdb_rating = data.get('imdb_rating', movie.imdb_rating)
    movie.overview = data.get('overview', movie.overview)
    movie.meta_score = data.get('meta_score', movie.meta_score)
    movie.director = data.get('director', movie.director)
    movie.star1 = data.get('star1', movie.star1)
    movie.star2 = data.get('star2', movie.star2)
    movie.star3 = data.get('star3', movie.star3)
    movie.star4 = data.get('star4', movie.star4)
    movie.no_of_votes = data.get('no_of_votes', movie.no_of_votes)
    movie.gross = data.get('gross', movie.gross)

    database.session.commit()
    return jsonify(movie.to_dict()), 200

@app.route('/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    """
    Delete a movie by ID
    ---
    tags:
        - Delete entry
    parameters:
        - name: id
          in: path
          type: integer
          required: true
          description: ID of the movie to delete
    responses:
        204:
          description: No content, movie deleted.
    """
    movie = Movie.query.get(id)
    if movie is None:
        return jsonify({'error': 'Movie not found'}), 404

    database.session.delete(movie)
    database.session.commit()
    return '', 204

### SWAGGER ###
@app.route('/spec')
def spec():
    """
    Endpoint to generate Swagger specification from the Flask app
    """
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Movie API"
    return jsonify(swag)

#URL paths for accessing the Swagger UI and specifications
SWAGGER_URL = '/swagger'
API_URL = '/spec'

#Swagger UI blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Movie API"
    }
)

#Register the Swagger UI blueprint on the Flask app
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

#Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
