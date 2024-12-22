import factory

from src.models.expense import Expense


class ExpenseFactory(factory.Factory):
    class Meta:
        model = Expense

    date = factory.Faker("date_time")
    category = factory.Faker("word")
    amount = factory.Faker("random_int", min=1, max=100)
    description = factory.Faker("sentence")
