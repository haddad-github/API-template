import psycopg2
import os
import pandas as pd
from dotenv import load_dotenv

#Load environment variables from .env file
load_dotenv()

#Database parameters from environment variables
DATABASE_PARAMS = {
    'database_name': os.getenv('DATABASE_NAME', 'movies_db'),
    'username': os.getenv('USERNAME', 'postgres'),
    'password': os.getenv('PASSWORD'),
    'host': os.getenv('DB_HOSTNAME', 'localhost'),
    'port': os.getenv('PORT', '5432')
}


def connect_to_database(DATABASE_PARAMS):
    """
    Connects to the PostgreSQL database
    """
    conn = psycopg2.connect(
        dbname=DATABASE_PARAMS['database_name'],
        user=DATABASE_PARAMS['username'],
        password=DATABASE_PARAMS['password'],
        host=DATABASE_PARAMS['host'],
        port=DATABASE_PARAMS['port']
    )
    return conn


def create_tables(conn):
    """
    Runs an SQL command to directly create the tables in the PostgreSQL database
    """
    commands = [
        """
        CREATE TABLE IF NOT EXISTS movies (
            id SERIAL PRIMARY KEY,
            poster_link TEXT,
            series_title TEXT NOT NULL,
            released_year INTEGER,
            certificate TEXT,
            runtime TEXT,
            genre TEXT,
            imdb_rating FLOAT,
            overview TEXT,
            meta_score INTEGER,
            director TEXT,
            star1 TEXT,
            star2 TEXT,
            star3 TEXT,
            star4 TEXT,
            no_of_votes INTEGER,
            gross TEXT
        );
        """
    ]

    #Execute SQL command to create the tables
    cur = conn.cursor()
    for command in commands:
        cur.execute(command)
    cur.close()
    conn.commit()
    print('Tables created!')


def populate_movies(csv, conn):
    """
    Populates the movies table in the PostgreSQL database based on the CSV
    """
    if not os.path.exists(csv):
        print(f"File {csv} does not exist.")
        return

    df = pd.read_csv(csv)
    df = df.fillna('NULL')

    #Ensure released_year column contains only valid integers
    df['Released_Year'] = pd.to_numeric(df['Released_Year'], errors='coerce').fillna(0).astype(int)

    #Convert meta_score to integer to match the database schema
    df['Meta_score'] = pd.to_numeric(df['Meta_score'], errors='coerce').fillna(0).astype(int)

    temp_csv = 'movies_temp.csv'
    df.to_csv(temp_csv, index=False, header=False)

    with open(temp_csv, 'r', encoding='utf-8') as file:
        with conn.cursor() as cur:
            cur.copy_expert(
                "COPY movies(poster_link, series_title, released_year, certificate, runtime, genre, imdb_rating, overview, meta_score, director, star1, star2, star3, star4, no_of_votes, gross) FROM STDIN WITH CSV",
                file)
            conn.commit()
    print('Populated the movies table!')

    #Delete the temporary CSV file
    if os.path.exists(temp_csv):
        os.remove(temp_csv)
        print(f"Deleted temporary file {temp_csv}.")


if __name__ == '__main__':
    #Connect to the database
    conn = connect_to_database(DATABASE_PARAMS=DATABASE_PARAMS)

    #Create the tables
    create_tables(conn=conn)

    #Populate the tables from the CSV
    csv_path = os.path.join('data', 'imdb_top_1000.csv')
    populate_movies(csv=csv_path, conn=conn)

    print("Database populated successfully!")

    #Close connection
    conn.close()
