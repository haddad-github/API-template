#!/bin/bash

#Function to prompt for input with a default value
prompt_with_default() {
  local prompt_message=$1
  local default_value=$2
  read -p "$prompt_message (Default: $default_value): " input_value
  echo ${input_value:-$default_value}
}

#Check if .env file exists
if [ ! -f .env ]; then
  echo ".env file not found. Let's create it."

  DATABASE_NAME=$(prompt_with_default "Enter DATABASE_NAME" "movies_db")
  USERNAME=$(prompt_with_default "Enter USERNAME" "postgres")

  read -p "Enter PASSWORD (Required): " PASSWORD
  if [ -z "$PASSWORD" ]; then
    echo "Password is required. Exiting."
    exit 1
  fi

  DB_HOSTNAME=$(prompt_with_default "Enter DB_HOSTNAME" "localhost")
  PORT=$(prompt_with_default "Enter PORT" "5432")
  SOURCE=$(prompt_with_default "Enter SOURCE" "postgresql")

  cat <<EOL > .env
DATABASE_NAME=$DATABASE_NAME
USERNAME=$USERNAME
PASSWORD=$PASSWORD
DB_HOSTNAME=$DB_HOSTNAME
PORT=$PORT
SOURCE=$SOURCE
EOL
  echo ".env file created."
fi

#Create a virtual environment if it doesn't exist
if [ ! -d "env" ]; then
  echo "Creating a virtual environment..."
  python3 -m venv env
fi

#Activate the virtual environment
echo "Activating the virtual environment..."
source env/bin/activate

#Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

#Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

#Load environment variables
echo "Loading environment variables..."
export $(grep -v '^#' .env | xargs)

#Function to execute SQL commands
invoke_sqlcmd() {
  local sql_query=$1
  PGPASSWORD=$PASSWORD psql -h $DB_HOSTNAME -p $PORT -U $USERNAME -d postgres -c "$sql_query"
}

#Create database and grant permissions
echo "Creating the database..."
create_db_sql="CREATE DATABASE $DATABASE_NAME;"
invoke_sqlcmd "$create_db_sql"

grant_privileges_sql="GRANT ALL PRIVILEGES ON DATABASE $DATABASE_NAME TO $USERNAME;"
invoke_sqlcmd "$grant_privileges_sql"

#Populate the database
echo "Populating the database..."
python3 ./database_creation/populate_database.py

#Run the API
echo "Starting the API..."
python3 ./api/app.py