#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to display help
show_help() {
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  up              Start all services (database, pgadmin)"
    echo "  down           Stop all services"
    echo "  restart        Restart all services"
    echo "  logs           Show logs for all services"
    echo "  db:reset       Reset the database (drop, create, migrate, seed)"
    echo "  db:migrate     Run database migrations"
    echo "  db:seed        Seed the database with test data"
    echo "  test           Run tests"
    echo "  shell          Open a shell in the app container"
    echo "  help           Show this help message"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
}

# Function to start services
start_services() {
    echo -e "${GREEN}Starting services...${NC}"
    docker-compose up -d
    echo -e "${GREEN}Services started!${NC}"
    echo -e "${YELLOW}PGAdmin is available at http://localhost:5050${NC}"
    echo -e "${YELLOW}API is available at http://localhost:8000${NC}"
}

# Function to stop services
stop_services() {
    echo -e "${YELLOW}Stopping services...${NC}"
    docker-compose down
    echo -e "${GREEN}Services stopped!${NC}"
}

# Function to restart services
restart_services() {
    stop_services
    start_services
}

# Function to show logs
show_logs() {
    docker-compose logs -f
}

# Function to reset the database
reset_database() {
    echo -e "${YELLOW}Resetting database...${NC}"
    docker-compose down -v
    docker-compose up -d postgres
    
    # Wait for postgres to be ready
    echo -e "${YELLOW}Waiting for PostgreSQL to be ready...${NC}"
    until docker-compose exec -T postgres pg_isready -U postgres; do
        sleep 1
    done
    
    # Run migrations
    run_migrations
    
    # Seed the database
    seed_database
    
    echo -e "${GREEN}Database reset complete!${NC}"
}

# Function to run migrations
run_migrations() {
    echo -e "${YELLOW}Running migrations...${NC}"
    # Install dependencies if needed
    pip install -r requirements/dev.txt
    # Run migrations
    alembic upgrade head
    echo -e "${GREEN}Migrations complete!${NC}"
}

# Function to seed the database
seed_database() {
    echo -e "${YELLOW}Seeding database...${NC}"
    # Run seed script
    python -m app.db.seed
    echo -e "${GREEN}Database seeded!${NC}"
}

# Function to run tests
run_tests() {
    echo -e "${YELLOW}Running tests...${NC}"
    # Install test dependencies if needed
    pip install -r requirements/test.txt
    # Run tests
    pytest tests/
}

# Function to open a shell in the app container
open_shell() {
    docker-compose exec app bash
}

# Main script logic
case "$1" in
    up)
        start_services
        ;;
    down)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    logs)
        show_logs
        ;;
    db:reset)
        reset_database
        ;;
    db:migrate)
        run_migrations
        ;;
    db:seed)
        seed_database
        ;;
    test)
        run_tests
        ;;
    shell)
        open_shell
        ;;
    help|--help|-h|*)
        show_help
        ;;
esac

exit 0
