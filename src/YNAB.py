# Will contain the code to interact with the YNAB API and retrieve the data
import requests
import os

YNAB_API_BASE_URL = os.getenv("YNAB_API_BASE_URL")
YNAB_BUDGET_ID = os.getenv("YNAB_BUDGET_ID")
YNAB_API_TOKEN = os.getenv("YNAB_API_TOKEN")

def get_ynab_data():
    url = f"{YNAB_API_BASE_URL}/budgets/{YNAB_BUDGET_ID}/categories"
    headers = {"Authorization": f"Bearer {YNAB_API_TOKEN}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
