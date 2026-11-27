# Korduroy Mosquito Backend

A REST API built with Flask, PostgreSQL, SQLAlchemy, JWT authentication, and Docker Compose. The project includes user registration, login, and listing management.

## Technologies

- Python
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- Flask-Migrate / Alembic
- JWT authentication
- Gunicorn
- Docker and Docker Compose

## Prerequisites

- Docker Desktop
- Docker Compose

Python and a local virtual environment are not required when running the application through Docker Compose.

## Environment Setup

Clone the repository and enter the project directory:

```bash
git clone https://github.com/jessicapaigeshirley-alt/korduroymosquito-backend.git
cd korduroymosquito-backend
```

Copy the example environment file:

```bash
cp .env.example .env
```

Configure these variables in `.env`:

- `JWT_SECRET`: A strong secret used to sign authentication tokens.
- `POSTGRES_PASSWORD`: A secure PostgreSQL database password.

The database connection URL is configured in `docker-compose.yml` and uses the PostgreSQL service name `db`.

Never commit your `.env` file or real credentials to GitHub.

## Running with Docker Compose

Build and start the application:

```bash
docker compose up --build -d
```

Docker Compose starts the Flask application and PostgreSQL database in separate containers. The application waits for the database health check before starting.

Check container status:

```bash
docker compose ps
```

The API is available at:

http://localhost:8001

## Database Migrations

Apply database migrations:

```bash
docker compose exec app flask --app 'my_backend:create_app("production")' db upgrade
```

This applies the existing Alembic migrations to the PostgreSQL database.

## Testing the API

### Health Check

```bash
curl -i http://localhost:8001/health
```

Expected HTTP status: `200 OK`.

### Register a User

```bash
curl -i -X POST http://localhost:8001/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test_user","email":"test@example.com","password":"Test123!"}'
```

Expected HTTP status: `201 CREATED`.

### Log In

```bash
curl -i -X POST http://localhost:8001/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test_user","password":"Test123!"}'
```

Expected HTTP status: `200 OK`, with an access token if authentication succeeds.

## Database Persistence

PostgreSQL data is stored in the `postgres_data` named Docker volume.

Stop the application:

```bash
docker compose down
```

Restart the application:

```bash
docker compose up -d
```

The named volume preserves database data between container restarts.

To remove the database volume and its stored data:

```bash
docker compose down -v
```

Use this command only when intentionally deleting the database data.

## Troubleshooting

Check application logs:

```bash
docker compose logs app --tail=100
```

Check database logs:

```bash
docker compose logs db --tail=100
```

Check container status:

```bash
docker compose ps
```

If the database connection fails, verify `POSTGRES_PASSWORD` in `.env` and confirm that the database container is healthy.