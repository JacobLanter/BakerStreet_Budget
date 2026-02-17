# Will contain the code to interact with the YNAB API and retrieve the data
import requests
import os

YNAB_API_BASE_URL = os.getenv("YNAB_API_BASE_URL")
YNAB_BUDGET_ID = os.getenv("YNAB_BUDGET_ID")
YNAB_API_TOKEN = os.getenv("YNAB_API_TOKEN")


def _milli_to_unit(value):
    """
    Convert YNAB milliunit values (e.g. 123450 for 123.45)
    into normal float currency amounts.
    Only convert raw integer milliunits, leave floats alone
    so we don't double-normalize.
    """
    if value is None:
        return None
    if isinstance(value, int):
        return value / 1000.0
    return value


def normalize_ynab_data(data):
    """
    Normalize only the known YNAB milliunit fields that we
    actually care about into normal float currency values.

    This keeps things fast and predictable for dashboards.
    """
    if not data or "data" not in data:
        return data

    category_groups = data["data"].get("category_groups", [])

    # Explicit list of milliunit fields on categories to convert
    milliunit_fields = [
        "budgeted",
        "activity",
        "balance",
        "goal_target",
        "goal_under_funded",
        "goal_overall_funded",
        "goal_overall_left",
        "goal_target_monthly",
        "goal_overall",  # kept from earlier list in case it's present
    ]

    for group in category_groups:
        for category in group.get("categories", []):
            for field in milliunit_fields:
                if field in category:
                    category[field] = _milli_to_unit(category.get(field))

    return data


def add_category_metrics(data):
    """
    Enrich the normalized YNAB JSON with derived percentage
    fields on each category so dashboards can use them directly.
    """
    if not data or "data" not in data:
        return data

    category_groups = data["data"].get("category_groups", [])

    for group in category_groups:
        for category in group.get("categories", []):
            # Skip hidden categories entirely
            if category.get("hidden"):
                continue

            goal_target_monthly = category.get("goal_target_monthly")
            goal_target = category.get("goal_target")
            target = goal_target_monthly if goal_target_monthly not in (None, 0) else goal_target
            balance = category.get("balance", 0) or 0

            # 1) Percent remaining for monthly spending envelopes:
            #    starts at 1.0 when the category is fully funded,
            #    then decreases towards 0 as you spend.
            if target not in (None, 0):
                percent_remaining_of_target = max(0.0, min(1.0, balance / target))
                percent_used_of_target = 1.0 - percent_remaining_of_target
            else:
                percent_remaining_of_target = None
                percent_used_of_target = None

            # 2) Percent to goal for long‑term savings:
            #    use overall goal fields when available so this
            #    increases from 0 → 1 as you save towards a big target.
            goal_overall = category.get("goal_overall")
            goal_overall_left = category.get("goal_overall_left")
            if goal_overall not in (None, 0) and goal_overall_left is not None:
                percent_to_goal = max(0.0, min(1.0, 1.0 - (goal_overall_left / goal_overall)))
            elif target not in (None, 0):
                # Fallback: use balance vs target if no overall fields
                percent_to_goal = max(0.0, min(1.0, balance / target))
            else:
                percent_to_goal = None

            category["percent_to_goal"] = percent_to_goal
            category["percent_remaining_of_target"] = percent_remaining_of_target
            category["percent_used_of_target"] = percent_used_of_target

    return data


def get_ynab_data():
    url = f"{YNAB_API_BASE_URL}/budgets/{YNAB_BUDGET_ID}/categories"
    headers = {"Authorization": f"Bearer {YNAB_API_TOKEN}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        raw = response.json()
        # Normalize all milliunit amounts to floats, then enrich
        # each category with derived percentage metrics.
        normalized = normalize_ynab_data(raw)
        enriched = add_category_metrics(normalized)
        return enriched
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def print_categories(data):
    """
    Take the JSON data returned from the YNAB API and
    print each category on its own line, with fields
    on that line separated by tabs.

    Expected structure (simplified):
    {
        "data": {
            "category_groups": [
                {
                    "name": "...",
                    "categories": [
                        {
                            "name": "...",
                            "balance": ...,
                            "budgeted": ...,
                            "activity": ...
                        },
                        ...
                    ]
                },
                ...
            ]
        }
    }
    """
    if not data:
        print("No data to display.")
        return

    category_groups = data.get("data", {}).get("category_groups", [])

    for group in category_groups:
        group_name = group.get("name", "Unknown Group")
        for category in group.get("categories", []):
            # Skip hidden categories
            if category.get("hidden"):
                continue

            # Use values already normalized + enriched on the category
            goal_target_monthly = category.get("goal_target_monthly")
            goal_target = category.get("goal_target")
            target = goal_target_monthly if goal_target_monthly not in (None, 0) else goal_target

            # Only keep categories that actually have a goal target
            if target in (None, 0):
                continue

            category_name = category.get("name", "Unknown Category")
            balance = category.get("balance", 0)
            percent_to_goal = category.get("percent_to_goal")
            percent_remaining_of_target = category.get("percent_remaining_of_target")
            percent_used_of_target = category.get("percent_used_of_target")

            # Pretty, labeled multi-line output so it's easy to read
            print("======================================")
            print(f"Group Name: {group_name}")
            print(f"Category Name: {category_name}")
            print(f"Target Goal: {target}")
            print(f"Current Balance: {balance}")
            print(f"Percent To Goal: {percent_to_goal}")
            print(f"Percent Remaining Of Target: {percent_remaining_of_target}")
            print(f"Percent Used Of Target: {percent_used_of_target}")
