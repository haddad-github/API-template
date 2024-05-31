# API-template
Simply run a script and have an API endpoint ready to go for any Frontend testing

## How to

*You need `PostgreSQL` installed

*You MUST enter your own postgre database user password yourself

Windows: Run `.\run_api_WINDOWS.ps1` in a Powershell command line

Linux: Run `chmod +x run_api_LINUX.sh` and then `.\run_api_LINUX.sh`

## Data

Source of the `imbd_top_1000.csv` in the `data/` folder comes from: https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows

It contains IMBD's top 1000 movies and includes the movie poster image link

## Database creation and population

Database is created and populated in the `database_creation` folder by `create_database.py` that creates the DB based on the .env variables and `populate_database.py`

## API

API is found in the `app.py` in the `api/` folder

It has full Swagger-UI integration

API URL by default: `localhost:5000`
Swagger-UI URL by default: `http://localhost:5000/swagger`