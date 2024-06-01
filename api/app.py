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
    Retrieve movies based on query parameters
    ---
    tags:
        - Full dump
    parameters:
        - name: series_title
          in: query
          type: string
          description: Title of the movie
        - name: released_year
          in: query
          type: integer
          description: Release year of the movie
        - name: runtime
          in: query
          type: string
          description: Runtime of the movie
        - name: runtime_lt
          in: query
          type: string
          description: Runtime less than
        - name: runtime_gt
          in: query
          type: string
          description: Runtime greater than
        - name: genre
          in: query
          type: string
          description: Genre of the movie
        - name: imdb_rating
          in: query
          type: number
          description: IMDb rating of the movie
        - name: imdb_rating_lt
          in: query
          type: number
          description: IMDb rating less than
        - name: imdb_rating_gt
          in: query
          type: number
          description: IMDb rating greater than
        - name: no_of_votes
          in: query
          type: integer
          description: Number of votes
        - name: no_of_votes_lt
          in: query
          type: integer
          description: Number of votes less than
        - name: no_of_votes_gt
          in: query
          type: integer
          description: Number of votes greater than
        - name: gross
          in: query
          type: string
          description: Gross earnings of the movie
        - name: gross_lt
          in: query
          type: string
          description: Gross earnings less than
        - name: gross_gt
          in: query
          type: string
          description: Gross earnings greater than
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
    query = Movie.query

    #Filter by series_title
    series_title = request.args.get('series_title')
    if series_title:
        query = query.filter(Movie.series_title.ilike(f"%{series_title}%"))

    #Filter by released_year
    released_year = request.args.get('released_year')
    if released_year:
        query = query.filter_by(released_year=released_year)

    #Filter by runtime
    runtime = request.args.get('runtime')
    if runtime:
        query = query.filter_by(runtime=runtime)

    runtime_lt = request.args.get('runtime_lt')
    if runtime_lt:
        query = query.filter(Movie.runtime < runtime_lt)

    runtime_gt = request.args.get('runtime_gt')
    if runtime_gt:
        query = query.filter(Movie.runtime > runtime_gt)

    #Filter by genre
    genre = request.args.get('genre')
    if genre:
        query = query.filter(Movie.genre.ilike(f"%{genre}%"))

    #Filter by imdb_rating
    imdb_rating = request.args.get('imdb_rating')
    if imdb_rating:
        query = query.filter_by(imdb_rating=imdb_rating)

    imdb_rating_lt = request.args.get('imdb_rating_lt')
    if imdb_rating_lt:
        query = query.filter(Movie.imdb_rating < imdb_rating_lt)

    imdb_rating_gt = request.args.get('imdb_rating_gt')
    if imdb_rating_gt:
        query = query.filter(Movie.imdb_rating > imdb_rating_gt)

    #Filter by number_of_votes
    no_of_votes = request.args.get('no_of_votes')
    if no_of_votes:
        query = query.filter_by(no_of_votes=no_of_votes)

    no_of_votes_lt = request.args.get('no_of_votes_lt')
    if no_of_votes_lt:
        query = query.filter(Movie.no_of_votes < no_of_votes_lt)

    no_of_votes_gt = request.args.get('no_of_votes_gt')
    if no_of_votes_gt:
        query = query.filter(Movie.no_of_votes > no_of_votes_gt)

    #Filter by gross
    gross = request.args.get('gross')
    if gross:
        query = query.filter_by(gross=gross)

    gross_lt = request.args.get('gross_lt')
    if gross_lt:
        query = query.filter(Movie.gross < gross_lt)

    gross_gt = request.args.get('gross_gt')
    if gross_gt:
        query = query.filter(Movie.gross > gross_gt)

    movies = query.all()
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
