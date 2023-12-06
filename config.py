import os

# Conection to Auth0
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
ALGORITHMS   = os.getenv("ALGORITHMS")
API_AUDIENCE = os.getenv("API_AUDIENCE")
#' #http://127.0.0.1:5000/login'
# https://dev-ookv36rq07kmjg5a.us.auth0.com/api/v2/


# Connection to DB
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASW")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Note: Enviroment setting on Render Variable in Webservice instant.
# If run from local.
# Please run setup.sh before. To settup ENV.