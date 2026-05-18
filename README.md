# BakerStreet Budget

BakerStreet Budget is a small Django dashboard I built to make my YNAB categories easier to review at a glance. Instead of opening YNAB and digging through category groups, the app syncs category data into PostgreSQL and gives me a focused view of saving goals, spending categories, and budget progress.

## Intended Use

This project is intended for local use only.

BakerStreet Budget is designed to run on your own machine with Docker Compose. It is not currently intended for public internet deployment, multi-user hosting, or shared cloud hosting.

Do not expose this application publicly without first adding production-grade security settings, reviewing authentication and authorization, disabling debug mode, configuring HTTPS, and protecting any synced YNAB financial data.

## Project Scope

The project is intentionally narrow: it is not trying to replace YNAB. It is a personal dashboard for the category information I care about most.

## What It Does

- Syncs category data from the YNAB API into a local PostgreSQL database.
- Stores category names, balances, budgeted amounts, activity, goal types, goal targets, and raw YNAB data.
- Filters out hidden, deleted, and internal YNAB categories.
- Displays selectable saving goals and spending goals on a dashboard.
- Uses Chart.js doughnut charts to show saving-goal progress.
- Includes a dashboard sync button that can refresh YNAB data from the app.
- Runs locally with Docker Compose.
- Loads secrets and runtime settings from environment variables.

## Why I Built It

I wanted a simple page that showed the YNAB categories I check most often without making budgeting feel heavier than it needs to be. The result is a lightweight dashboard that pulls in real YNAB data and presents the useful parts in one place.

## Tech Stack

- Python
- Django
- PostgreSQL
- Docker Compose
- YNAB API
- Chart.js

I used Codex and ChatGPT as development assistants while building this project, mainly for debugging, refactoring, and thinking through Django and Docker configuration.

## Project Structure

```text
BakerStreet_Budget/
  budget/
    management/commands/sync_ynab_categories.py
    templates/budget/dashboard.html
    templates/budget/category_list.html
    models.py
    urls.py
    utils.py
    views.py
  config/
    settings.py
    urls.py
  docker-compose.yml
  Dockerfile
  requirements.txt
  manage.py
  .env.example
```

## Environment Variables

Copy the example file and fill in your local values:

```bash
cp .env.example .env
```

Required values:

```env
SECRET_KEY=replace-me
DEBUG=True

POSTGRES_DB=bakerstreet_budget
POSTGRES_USER=bakerstreet_user
POSTGRES_PASSWORD=replace-me
DB_HOST=db
DB_PORT=5432

YNAB_BEARER_TOKEN=replace-me
YNAB_BUDGET_ID=last-used

ALLOWED_HOSTS=localhost,127.0.0.1
```

For access from another device on your local network, add your machine's local IP:

```env
ALLOWED_HOSTS=192.168.1.201,localhost,127.0.0.1
```

Keep `.env` out of Git. `.env.example` should only contain placeholders.

## Running Locally

Build and start the app:

```bash
docker compose up --build
```

Run migrations:

```bash
docker compose exec web python manage.py migrate
```

Create an admin user:

```bash
docker compose exec web python manage.py createsuperuser
```

Sync YNAB categories:

```bash
docker compose exec web python manage.py sync_ynab_categories
```

Open the dashboard:

```text
http://localhost:8000/dashboard/
```

## Main Routes

```text
/dashboard/
/category_list/
/admin/
```

## Notes

YNAB stores money values in milliunits:

```text
1000 milliunits = $1.00
```

The app keeps the original YNAB values in the database and formats them for display where needed.
