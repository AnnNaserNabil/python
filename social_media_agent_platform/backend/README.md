# Social Media Agent Platform - Backend

This is the backend service for the Social Media Agent Platform, built with FastAPI and PostgreSQL.

## Features

- **User Authentication**: JWT-based authentication with OAuth2 support
- **Agent Management**: Create, update, and manage AI agents
- **Social Media Integration**: Connect and manage multiple social media accounts
- **Vector Store**: Store and search embeddings with support for multiple vector databases
- **File Uploads**: Handle file uploads with size and type validation
- **Rate Limiting**: Protect your API from abuse
- **CORS**: Secure cross-origin resource sharing

## Prerequisites

- Python 3.10+
- PostgreSQL 13+
- Docker (optional, for development)

## Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/social-media-agent-platform.git
cd social-media-agent-platform/backend
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements/dev.txt
```

4. **Set up environment variables**

Create a `.env` file in the backend directory:

```bash
cp .env.example .env
```

Update the values in `.env` as needed.

5. **Set up the database**

Using Docker (recommended for development):

```bash
docker-compose up -d postgres
```

Or manually create a PostgreSQL database and update the `DATABASE_URL` in `.env`.

6. **Run migrations**

```bash
alembic upgrade head
```

7. **Seed the database (optional)**

```bash
python -m app.db.seed
```

## Running the Application

### Development

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Production

For production, use Gunicorn with Uvicorn workers:

```bash
gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 app.main:app
```

## API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Testing

```bash
pytest
```

## Code Style

```bash
# Format code with Black and isort
black .
isort .

# Check for style issues
flake8

# Run type checking
mypy .
```

## Deployment

### Docker

Build the Docker image:

```bash
docker build -t social-media-agent-backend .
```

Run the container:

```bash
docker run -d --name social-agent-backend -p 8000:8000 --env-file .env social-media-agent-backend
```

### Kubernetes

See the `kubernetes/` directory for example Kubernetes manifests.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `False` |
| `SECRET_KEY` | Secret key for JWT tokens | `your-secret-key-change-this-in-production` |
| `DATABASE_URL` | Database connection URL | `postgresql://postgres:postgres@localhost:5432/social_agent` |
| `FIRST_SUPERUSER` | Email of the first superuser | `admin@example.com` |
| `FIRST_SUPERUSER_PASSWORD` | Password for the first superuser | `changethis` |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `VECTOR_STORE_TYPE` | Vector store type (`postgres`, `pinecone`, `weaviate`) | `postgres` |
| `POSTGRES_VECTOR_DB_URL` | PostgreSQL vector database URL | - |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
