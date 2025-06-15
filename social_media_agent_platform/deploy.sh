#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for Docker
if ! command_exists docker; then
    echo -e "${RED}Docker is not installed. Please install Docker and try again.${NC}" >&2
    exit 1
fi

# Check for Docker Compose
if ! command_exists docker-compose; then
    echo -e "${RED}Docker Compose is not installed. Please install Docker Compose and try again.${NC}" >&2
    exit 1
fi

# Function to deploy the application
deploy() {
    echo -e "${YELLOW}Starting deployment...${NC}"
    
    # Build and start containers
    echo -e "${YELLOW}Building and starting containers...${NC}"
    docker-compose up -d --build
    
    # Wait for services to be ready
    echo -e "${YELLOW}Waiting for services to be ready...${NC}"
    sleep 10
    
    # Run database migrations
    echo -e "${YELLOW}Running database migrations...${NC}"
    docker-compose exec backend alembic upgrade head
    
    # Seed the database
    echo -e "${YELLOW}Seeding the database...${NC}"
    docker-compose exec backend python -m app.db.seed
    
    echo -e "${GREEN}Deployment completed successfully!${NC}"
    echo -e "\n${YELLOW}Access the application at:${NC}"
    echo -e "- Frontend: http://localhost:3000"
    echo -e "- Backend API: http://localhost:8000"
    echo -e "- API Documentation: http://localhost:8000/docs"
    echo -e "- PGAdmin: http://localhost:5050"
}

# Function to stop the application
stop() {
    echo -e "${YELLOW}Stopping application...${NC}"
    docker-compose down
    echo -e "${GREEN}Application stopped.${NC}"
}

# Function to view logs
logs() {
    docker-compose logs -f
}

# Function to show help
show_help() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  deploy      Deploy the application"
    echo "  stop        Stop the application"
    echo "  logs        View logs"
    echo "  help        Show this help message"
    echo ""
    echo "If no command is provided, 'deploy' will be used as default."
}

# Main script logic
case "$1" in
    deploy)
        deploy
        ;;
    stop)
        stop
        ;;
    logs)
        logs
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        deploy
        ;;
esac

exit 0
