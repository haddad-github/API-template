import psycopg2
import os
from dotenv import load_dotenv

#Load environment variables from .env file
load_dotenv()

#Database parameters
DATABASE_PARAMS = {
    'database_name': os.getenv('DATABASE_NAME', 'movies_db'),
    'username': os.getenv('USERNAME', 'postgres'),
    'password': os.getenv('PASSWORD', '123'),
    'host': os.getenv('DB_HOSTNAME', 'localhost'),
    'port': os.getenv('PORT', '5432')
}

def create_postgresql_database(DATABASE_PARAMS):
    """
    Creates a PostgreSQL database (initializes it)

    :param DATABASE_PARAMS: dictionary that contains the database parameters
    """
    #Before creating a database, need to connect to the default one first
    conn = psycopg2.connect(
        dbname='postgres',
        user=DATABASE_PARAMS['username'],
        password=DATABASE_PARAMS['password'],
        host='localhost',
        port='5432'
    )

    #Autocomit On and initiate the SQL injector
    conn.autocommit = True
    cur = conn.cursor()

    #Execute database creation
    try:
        cur.execute(f"CREATE DATABASE {DATABASE_PARAMS['database_name']}")
        print(f'Database {DATABASE_PARAMS["database_name"]} successfully created')
    except psycopg2.Error as e:
        print(e)

    #Close the connection
    cur.close()
    conn.close()

if __name__ == '__main__':
    create_postgresql_database(DATABASE_PARAMS=DATABASE_PARAMS)