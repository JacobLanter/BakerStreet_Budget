# BakerStreet Budget

BakerStreet Budget is a learning project for building a focused Django/PostgreSQL dashboard that syncs category data from the YNAB API and visualizes budget progress.

The goal is not to start with a finished app. The goal is to give you a clean project map so you can build the pieces yourself and understand what each part is doing.

## MVP Goal

Build a dashboard that:

- Connects Django to PostgreSQL with Docker Compose
- Loads secrets and settings from environment variables
- Calls the YNAB API
- Syncs budget, category group, and category data into local models
- Converts YNAB milliunits into `Decimal` dollar amounts
- Calculates budget progress values in a service layer
- Renders a dashboard with summary cards, progress bars, and one Chart.js chart

## File Structure

Current starter scaffold:

```text
BakerStreet_Budget/
  docker-compose.yml
  Dockerfile
  requirements.txt
  manage.py
  config/
  budget/
  .env
  .env.example
  .gitignore
  README.md
```

Notes:

- `.env` is for local secrets and should not be committed.
- `.env.example` documents the environment variables the project needs.
- `config/` is the Django project settings folder.
- `budget/` is the Django app folder.
- `.dockerignore` may also exist as a Docker helper, but it does not need to be part of the main learning structure.

Inside `config/`, Django will eventually have:

```text
config/
  __init__.py
  settings.py
  urls.py
  asgi.py
  wsgi.py
```

Inside `budget/`, start small:

```text
budget/
  __init__.py
  admin.py
  apps.py
  models.py
  views.py
  migrations/
```

Files to add later, when you reach that step:

```text
budget/urls.py
budget/forms.py
budget/services/ynab_client.py
budget/services/ynab_sync.py
budget/services/progress.py
budget/management/commands/sync_ynab.py
budget/templates/budget/base.html
budget/templates/budget/dashboard.html
budget/templates/budget/category_list.html
budget/templates/budget/sync.html
static/css/styles.css
static/js/charts.js
```

## What Each Piece Is For

`config/settings.py`  
Configure Django, PostgreSQL, static files, and environment variables.

`budget/models.py`  
Define `YnabBudget`, `CategoryGroup`, and `Category`.

`budget/views.py`  
Start with a simple placeholder view later, then connect it to templates and services.

## YNAB Endpoint

Use this endpoint for the MVP:

```text
GET /budgets/{budget_id}/categories
```

Start with:

```text
YNAB_BUDGET_ID=last-used
```

## Money Conversion

YNAB returns money in milliunits:

```text
1000 milliunits = $1.00
```

Use `Decimal`, not float.

## Minimal First Steps

1. Make Django boot locally in Docker.
2. Load `.env` values in `config/settings.py`.
3. Configure PostgreSQL in `settings.py` using the `DB_*` environment variables.
4. Add `budget` to `INSTALLED_APPS`.
5. Run `python manage.py check`.
6. Run the first migration command against Postgres.

After that, add the app pieces one at a time:

1. Models
2. Admin
3. YNAB client
4. Sync service
5. Management command
6. Progress service
7. Views and URLs
8. Templates
9. Static CSS and Chart.js

## Development Commands

These commands are the target workflow once you have filled in the Django entrypoint and settings.

```bash
docker compose up --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose down
```

## Environment Variables

Copy `.env.example` to `.env` when you are ready to run locally:

```bash
cp .env.example .env
```

Then fill in your real values, especially:

```text
YNAB_ACCESS_TOKEN=replace-me
YNAB_BUDGET_ID=last-used
```

Keep `.env` out of Git.

## Interview Framing

I built BakerStreet Budget as a Django/PostgreSQL dashboard that visualizes budget progress from real YNAB category data. Instead of trying to recreate YNAB, I scoped the project around one focused workflow: syncing category data from the YNAB API, storing it locally, calculating progress values, and displaying those values through progress bars and charts.
