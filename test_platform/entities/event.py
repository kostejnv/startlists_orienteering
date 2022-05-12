from test_platform.entities.athlete import Athlete
from test_platform.entities.category import Category


class Event:
    def __init__(self, id, name, date, discipline, region):
        self.name = name
        self.date = date
        self.discipline = discipline
        self.id = id
        self.region = region
        self.categories = {}
        self.capacity = -1

    def get_not_empty_categories_with_interval_start(self):
        return {name: category for name, category in self.categories.items() if
                category.has_interval_start and category.get_category_count() > 0}
