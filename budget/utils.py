
# Helper method converts the milliunits from YNAB into standard Dollar format
def format_milliunits(amount):
    if amount is None:
        return ""

    return f"${amount / 1000:,.2f}"

# Helper function converts target based goals into percentage data for dashboard charts
def build_goal_charts(categories):

    goal_charts = [] 

    for category in categories:
        if category.goal_target is not None and category.goal_target > 0:
            percentage = (category.balance / category.goal_target) * 100
        else:
            percentage = 0

        percentage = min(max(percentage, 0), 100)

        goal_charts.append({
            "name": category.name,
            "percentage": round(percentage, 2),
            "remaining": round(100 - percentage, 2),
        })

    return goal_charts