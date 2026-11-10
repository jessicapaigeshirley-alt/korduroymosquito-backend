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
