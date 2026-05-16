from django.db import models

# Defines the structure of one budget category record.
# Django uses this model to create a PostgreSQL table where each row is one category.
class Category(models.Model):
    ynab_id = models.UUIDField(unique=True)

    category_group_id = models.UUIDField()
    category_group_name = models.CharField(max_length=100)

    name = models.CharField(max_length=100)

    hidden = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    budgeted = models.BigIntegerField()
    activity = models.BigIntegerField()
    balance = models.BigIntegerField()

    goal_type = models.CharField(max_length=20, blank=True, null=True)
    goal_target = models.BigIntegerField(blank=True, null=True)

    raw_data = models.JSONField()

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category_group_name}: {self.name}"

    # Helper method converts the milliunits from YNAB into standard Dollar format
    def format_milliunits(self, amount):
        if amount is None:
            return ""

        return f"${amount / 1000:,.2f}"

    # @property treats methods like an attribute of the table not as a function. EX: category.balance.display
    @property
    def balance_display(self):
        return self.format_milliunits(self.balance)

    @property
    def budgeted_display(self):
        return self.format_milliunits(self.budgeted)

    @property
    def activity_display(self):
        return self.format_milliunits(self.activity)

    @property
    def goal_target_display(self):
        return self.format_milliunits(self.goal_target)
