from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from .models import Category
from .utils import build_goal_charts

# Runs the YNAB category sync command from the dashboard sync button.
@login_required
def sync_ynab_now(request):
    if request.method == "POST":
        call_command("sync_ynab_categories")

    return redirect("dashboard")

# Displays list of active budget categories
def category_list(request):
    categories = Category.objects.filter(
    hidden=False,
    deleted=False,
    ).exclude(
        category_group_name="Internal Master Category"
    )
    return render(request, "budget/category_list.html", {"categories" : categories},)

# Displays selected saving and spending goals on the dashboard.
def dashboard(request):
    
    # ----- Base categories -----

    categories = Category.objects.filter(
    hidden=False,
    deleted=False,
    ).exclude(
        category_group_name="Internal Master Category"
    )

    # ----- Saving Goal -----

    target_goals = categories.filter(
    goal_type__in=["TB", "TBD"]
    )

    selected_target_category_ids = request.GET.getlist("target_categories")

    selected_target_categories = target_goals.filter(
    id__in=selected_target_category_ids
    )

    selected_target_goal_charts = build_goal_charts(selected_target_categories)

    # ----- Spending Goals -----

    spending_goals = categories.filter(
    goal_type="NEED"
    )

    selected_need_category_ids = request.GET.getlist("need_categories")

    selected_need_categories = spending_goals.filter(
        id__in=selected_need_category_ids
    )
    

    # ----- Render -----

    return render(request, "budget/dashboard.html", {
        "target_goals": target_goals,
        "spending_goals": spending_goals,
        "selected_target_goal_charts": selected_target_goal_charts,
        "selected_need_categories": selected_need_categories,
        "selected_target_category_ids": selected_target_category_ids,
        "selected_need_category_ids": selected_need_category_ids,
    })