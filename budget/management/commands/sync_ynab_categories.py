import os
import ynab
import json
from django.core.management.base import BaseCommand
from budget.models import Category


class Command(BaseCommand):

    # help informs what this base commands intended workflow is
    help = "Sync YNAB categories into the local database"

    # The handle is the method that runs when sync_ynab_categories is called
    def handle(self, *args, **options):

        api_response = self.extract_categories()

        if api_response is None:
            self.stderr.write(self.style.ERROR("Failed to fetch YNAB categories."))
            return

        category_groups = api_response.data.category_groups

        loaded_count = 0
        failed_count = 0

        for group in category_groups:
            for category in group.categories:
                try:
                    self.load_category(category)
                    loaded_count += 1

                except Exception as e:
                    self.stderr.write(
                        self.style.ERROR(f"Exception when trying to load category into PostgreSQL: {e}")
                    )
                    failed_count += 1

        self.stdout.write(
                    self.style.SUCCESS(f"Successfully loaded {loaded_count} categories into PostgreSQL. Failed to load {failed_count} categories.")
                )
    
    # Helper method that will reach out to YNAB to grab all category data
    def extract_categories(self):

        access_token = os.environ.get("YNAB_BEARER_TOKEN")

        if not access_token:
            self.stderr.write(self.style.ERROR("YNAB_BEARER_TOKEN is missing."))
            return None

        budget_id = os.environ.get("YNAB_BUDGET_ID")

        if not budget_id:
            self.stderr.write(self.style.ERROR("YNAB_BUDGET_ID is missing."))
            return None

        configuration = ynab.Configuration(
            host = "https://api.ynab.com/v1",
            access_token = access_token
        )

        # Enter a context with an instance of the API client
        with ynab.ApiClient(configuration) as api_client:
            # Create an instance of the API class
            api_instance = ynab.CategoriesApi(api_client)

            try:
                # Get all categories
                api_response = api_instance.get_categories(budget_id)
                return api_response
                
            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(f"Exception when calling CategoriesApi.get_categories: {e}")
                )
                return None
    
    # Helper method that will load one category data into PostgreSQL
    def load_category(self, category_data):

        raw_data = json.loads(category_data.to_json())

        Category.objects.update_or_create(
            ynab_id=category_data.id,
            defaults={
                "category_group_id": category_data.category_group_id,
                "category_group_name": category_data.category_group_name,
                "name": category_data.name,
                "hidden": category_data.hidden,
                "deleted": category_data.deleted,
                "budgeted": category_data.budgeted,
                "activity": category_data.activity,
                "balance": category_data.balance,
                "goal_type": category_data.goal_type,
                "goal_target": category_data.goal_target,
                "raw_data": raw_data,
            },
        )