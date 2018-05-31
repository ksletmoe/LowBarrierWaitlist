#!/usr/bin/env bash

set -e

if [ -z ${MONGO_DB_DIR+x} ]; then
    export MONGO_DB_DIR="./.db"
fi
mongod --dbpath "$MONGO_DB_DIR"
