#!/bin/bash

DB_PATH=$(pwd)/../db
echo $DB_PATH

docker-compose -f maria_db-compose.yml down
docker-compose -f maria_db-compose.yml up -d
