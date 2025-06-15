#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create extensions
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE EXTENSION IF NOT EXISTS "pgcrypto";
    CREATE EXTENSION IF NOT EXISTS "vector";
    
    -- Enable row-level security
    ALTER DATABASE $POSTGRES_DB SET "app.jwt_secret" TO 'your-secret-key-change-this-in-production';
    
    -- Create custom types if needed
    CREATE TYPE user_role AS ENUM ('admin', 'user', 'agent');
    CREATE TYPE social_platform AS ENUM ('twitter', 'facebook', 'linkedin', 'instagram');
    
    -- Grant permissions
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;
EOSQL

echo "Database initialization complete!"
