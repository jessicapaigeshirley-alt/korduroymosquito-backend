# Backend Project — Flask API

This project is a REST API built with Flask, PostgreSQL, SQLAlchemy, JWT authentication, and Docker Compose. It includes user registration, login, and authenticated listing management.

## Prerequisites

- Docker
- Docker Compose

Python and a virtual environment are not required to run the application with Docker Compose.

## Environment Setup

1. Clone the repository.
2. Copy `.env.example` to `.env`:

   ```bash
   cp .env.example .env
   ```

3. Configure these environment variables:

   - `JWT_SECRET`: A strong random secret used to sign authentication tokens.
   - `POSTGRES_PASSWORD`: The password for the PostgreSQL database.

   `DATABASE_URL` does not need to be defined in `.env` for Docker Compose because it is configured in `docker-compose.yml`.

   The `.env` file should be ignored by Git to protect secrets. The `.env.example` file should be committed without real credentials.

## Start the Application

Run:

```bash
docker compose up --build -d
```

Verify both containers:

```bash
docker compose ps
```

The application runs at:

`http://127.0.0.1:8001`

The Flask application runs through Gunicorn, and PostgreSQL runs in a separate container.

## Database Migrations

Apply migrations inside the application container:

```bash
docker compose exec app flask --app 'my_backend:create_app("production")' db upgrade
```

This creates and updates the required PostgreSQL tables.

## Verify the API

### Health Check

```bash
curl -i http://127.0.0.1:8001/health
```

Expected response:

```json
{"status":"ok"}
```

HTTP status: `200 OK`

### Register a User

```bash
curl -i -X POST http://127.0.0.1:8001/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "email": "test@example.com",
    "password": "Test123!"
  }'
```

Expected status: `201 CREATED`

The response contains the new user's ID, username, and email.

### Log In

```bash
curl -i -X POST http://127.0.0.1:8001/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "password": "Test123!"
  }'
```

Expected status: `200 OK`

The response includes an `access_token` and `token_type` of `Bearer`.

## Database Persistence

To stop the application:

```bash
docker compose down
```

To restart:

```bash
docker compose up -d
```

PostgreSQL data is stored in the `postgres_data` named volume, so existing users and listings survive container removal and recreation.

To verify persistence, register a user, shut down and restart Compose, and log in with the same credentials.

Do not use `docker compose down -v` unless you intentionally want to remove the database volume.

## Troubleshooting

- **Port conflict:** Check the `ports` mapping in `docker-compose.yml`. This project uses `8001:8000`.
- **Database connection failure:** Verify `POSTGRES_PASSWORD` in `.env` and check database health with `docker compose ps`.
- **Application errors:** Run `docker compose logs app --tail=100`.
- **Database errors:** Run `docker compose logs db --tail=100`.
- **Missing tables:** Run the database migration command again.

## Technologies Used

- Python and Flask
- PostgreSQL
- Flask-SQLAlchemy
- Flask-Migrate / Alembic
- JWT authentication
- Gunicorn
- Docker and Docker Compose
# Korduroy Mosquito Backend

This is the Flask backend for my Korduroy Mosquito project.

## Technologies
- Python
- Flask
- SQLAlchemy
- SQLite

## Project Features
- Application factory configuration
- Environment variables for sensitive settings
- Listings API endpoint

## Development
This project is currently under development.

## Unit 1 Setup

To create a virtual environment, run:

python3 -m venv venv

To activate it on macOS, run:

source venv/bin/activate

## Setup

After downloading or cloning this project, I create and activate a Python virtual environment. Then I install the project dependencies:

```bash
pip install -r requirements.txt
```

To start my Flask application in development mode, I run:

```bash
flask --app 'my_backend:create_app("development")' run
```

The application runs locally at http://127.0.0.1:5000.

## Environment Variables

I copy the example environment file to create my own local settings:

```bash
cp .env.example .env
```

I set `JWT_SECRET` to a strong secret value for signing authentication tokens. I use `DATABASE_URL` to tell Flask which database to connect to. I keep `.env` private and do not upload it to GitHub.

## Database and Migrations

My project uses SQLAlchemy and has Flask-Migrate initialized. I haven't created or run any database migrations yet. The development configuration uses SQLite, and the database setup process still needs to be documented and tested.
