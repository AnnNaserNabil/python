#!/bin/bash

# Database configuration
DB_NAME="social_agent"
DB_USER="postgres"
DB_PASSWORD="postgres"
DB_HOST="localhost"
DB_PORT="5432"

# Check if PostgreSQL is running
if ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER > /dev/null 2>&1; then
  echo "PostgreSQL is not running or not accessible. Please start PostgreSQL and try again."
  exit 1
fi

# Create database if it doesn't exist
if ! psql -h $DB_HOST -p $DB_PORT -U $DB_USER -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
  echo "Creating database $DB_NAME..."
  createdb -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME
  if [ $? -ne 0 ]; then
    echo "Failed to create database $DB_NAME"
    exit 1
  fi
  echo "Database $DB_NAME created successfully"
else
  echo "Database $DB_NAME already exists"
fi

# Create vector extension if using PostgreSQL
if [ "$VECTOR_STORE_TYPE" = "postgres" ]; then
  echo "Setting up pgvector extension..."
  psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "CREATE EXTENSION IF NOT EXISTS vector;"
  if [ $? -ne 0 ]; then
    echo "Failed to create pgvector extension"
    exit 1
  fi
  echo "pgvector extension created successfully"nfi

echo "Database setup complete"
exit 0
