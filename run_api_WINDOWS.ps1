#RUN_THIS_TO_RUN_API.ps1
$envFilePath = ".env"

#Check if .env file exists
if (-Not (Test-Path $envFilePath)) {
    Write-Host ".env file not found. Let's create it."
    $dbName = Read-Host "Enter DATABASE_NAME (Default: movies_db)"
    $username = Read-Host "Enter USERNAME (Default: postgres)"
    $password = Read-Host "Enter PASSWORD (Required)"
    if (-Not $password) {
        Write-Host "Password is required. Exiting."
        exit
    }
    $dbHost = Read-Host "Enter DB_HOSTNAME (Default: localhost)"
    $port = Read-Host "Enter PORT (Default: 5432)"
    $source = Read-Host "Enter SOURCE (Default: postgresql)"

    $dbName = if ($dbName) { $dbName } else { "movies_db" }
    $username = if ($username) { $username } else { "postgres" }
    $dbHost = if ($dbHost) { $dbHost } else { "localhost" }
    $port = if ($port) { $port } else { "5432" }
    $source = if ($source) { $source } else { "postgresql" }

    $envContent = @"
DATABASE_NAME=$dbName
USERNAME=$username
PASSWORD=$password
DB_HOSTNAME=$dbHost
PORT=$port
SOURCE=$source
"@

    $envContent | Out-File -FilePath $envFilePath -Encoding utf8
    Write-Host ".env file created."
}

#Create and activate virtual environment
if (-Not (Test-Path "env")) {
    Write-Host "Creating a virtual environment..."
    python -m venv env
}

Write-Host "Activating the virtual environment..."
& env\Scripts\Activate

#Upgrade pip and install requirements
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

Write-Host "Installing requirements..."
pip install -r requirements.txt

#Load environment variables
Write-Host "Loading environment variables..."
$env:DATABASE_NAME = (Get-Content .env | Select-String -Pattern '^DATABASE_NAME=').ToString().Split('=')[1].Trim()
$env:USERNAME = (Get-Content .env | Select-String -Pattern '^USERNAME=').ToString().Split('=')[1].Trim()
$env:PASSWORD = (Get-Content .env | Select-String -Pattern '^PASSWORD=').ToString().Split('=')[1].Trim()
$env:DB_HOSTNAME = (Get-Content .env | Select-String -Pattern '^DB_HOSTNAME=').ToString().Split('=')[1].Trim()
$env:PORT = (Get-Content .env | Select-String -Pattern '^PORT=').ToString().Split('=')[1].Trim()
$env:SOURCE = (Get-Content .env | Select-String -Pattern '^SOURCE=').ToString().Split('=')[1].Trim()

# Function to execute SQL commands
function Invoke-SqlCmd {
    param (
        [string]$SqlQuery,
        [string]$User,
        [string]$Password
    )
    $connectionString = "Host=$env:DB_HOSTNAME;Port=$env:PORT;User Id=$User;Password=$Password;Database=postgres"
    $psqlPath = "C:\Program Files\PostgreSQL\15\bin\psql.exe"
    $env:PGPASSWORD = $Password
    & $psqlPath -c $SqlQuery --username=$User --host=$env:DB_HOSTNAME --port=$env:PORT
    Remove-Item Env:PGPASSWORD
}

#Create database and grant permissions
Write-Host "Creating the database..."
$createDbSql = "CREATE DATABASE $env:DATABASE_NAME;"
Invoke-SqlCmd -SqlQuery $createDbSql -User $env:USERNAME -Password $env:PASSWORD

$grantPrivilegesSql = "GRANT ALL PRIVILEGES ON DATABASE $env:DATABASE_NAME TO $env:USERNAME;"
Invoke-SqlCmd -SqlQuery $grantPrivilegesSql -User $env:USERNAME -Password $env:PASSWORD

#Populate the database
Write-Host "Populating the database..."
python .\database_creation\populate_database.py

#Run the API
Write-Host "Starting the API..."
python .\api\app.py
