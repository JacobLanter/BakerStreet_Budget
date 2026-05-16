from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from .models import Category

@login_required
def sync_ynab_now(request):
    if request.method == "POST":
        call_command("sync_ynab_categories")

    return redirect("dashboard")

def category_list(request):
    categories = Category.objects.filter(
        hidden=False,
        deleted=False,
    ).exclude(
        category_group_name="Internal Master Category"
    )

    return render(request, "budget/category_list.html", {"categories" : categories},)

def dashboard(request):
    categories = Category.objects.filter(
        hidden=False,
        deleted=False,
    ).exclude(
        category_group_name="Internal Master Category"
    )

    target_goals = categories.filter(
    goal_type__in=["TB", "TBD"]
    )

    target_goal_charts = []

    for category in target_goals:
        if category.goal_target is not None and category.goal_target > 0:
            percentage = (category.balance / category.goal_target) * 100
        else:
            percentage = 0

        target_goal_charts.append({
            "name": category.name,
            "percentage": round(percentage, 2),
            "remaining": round(100 - percentage, 2),
        })

    spending_goals = categories.filter(
    goal_type="NEED"
    )

    selected_need_category_ids = request.GET.getlist("need_categories")

    selected_need_categories = spending_goals.filter(
        id__in=selected_need_category_ids
    )
    
    selected_need_goal_charts = []

    for category in selected_need_categories:
        if category.goal_target is not None and category.goal_target > 0:
            percentage = (category.balance / category.goal_target) * 100
        else:
            percentage = 0

        selected_need_goal_charts.append({
            "name": category.name,
            "percentage": round(percentage, 2),
            "remaining": round(100 - percentage, 2),
        })

    return render(request, "budget/dashboard.html", {
        "categories": categories,
        "target_goals": target_goals,
        "spending_goals": spending_goals,
        "target_goal_charts": target_goal_charts,
        "selected_need_category_ids": selected_need_category_ids,
        "selected_need_categories": selected_need_categories,
        "selected_need_goal_charts": selected_need_goal_charts,
    })