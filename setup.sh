#!/bin/bash
export DATABASE_URL="postgresql://postgres@localhost:5432/postgres"
export EXCITED="true"

# Conection to Auth0
export AUTH0_DOMAIN="https://dev-ookv36rq07kmjg5a.us.auth0.com/api/v2/"
export ALGORITHMS=['RS256']
export API_AUDIENCE="http://127.0.0.1:5000/"


# Connection to DB
export DB_NAME="examdb_uyig"
export DB_USER="adm"
export DB_PASW="UvZK7UQhUbtZXccphztAIQjrenDNn71o"
export DB_HOST="dpg-clo7u6uqc21c73e48vl0-a.singapore-postgres.render.com"
export DB_PORT="5432"
#export SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
export SQLALCHEMY_TRACK_MODIFICATIONS=False

echo "setup.sh script executed successfully!"
FLASK_APP=exam_main FLASK_DEBUG=true flask run