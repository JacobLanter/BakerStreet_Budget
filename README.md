# YNAB_Dashboard

This project pulls data from a user's YNAB account using the YNAB API and converts all active budget and goal values into percentages before storing or visualizing anything. Instead of keeping dollar amounts, categories like eating out or discretionary spending are represented only by the percentage remaining, so no raw financial data is saved.

The backend processes both short-term budget categories and long-term goals, such as retirement savings and paying off a house, and indexes those percentage-based metrics into Elasticsearch. Kibana is then used to build a simple dashboard that highlights the most important metrics at a glance.

The goal is to create a passive, read-only dashboard that can be displayed on a thin wall-mounted TV, making it easy to quickly see progress toward goals and remaining budget percentages without exposing actual money values.

## System Overview

This project consists of a small backend service that retrieves data from the YNAB API, converts monetary values into percentage-based metrics, and publishes these metrics for visualization. Elasticsearch is used to store the processed metrics, and Kibana is used to build a read-only dashboard for display.

The services are intended to run locally using Docker Compose, with each component isolated into its own container. This setup is designed for personal use and local visualization rather than production deployment.

## Tech Stack

Backend: Python \
Data Store: Elasticsearch \
Visualization: Kibana \
Orchestration: Docker Compose \
External API: YNAB API

## Development Notes

This project is developed with the assistance of AI-powered coding tools, including Cursor, to improve iteration speed and code quality. All design decisions, architecture, and final implementations are reviewed and controlled manually.
