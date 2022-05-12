import json
from test_platform.entities.category import Category


class Classes_manager:
    def __init__(self, event_f):
        self.classes = json.load(event_f)["Classes"]

    def get_categories(self):
        cats = {cat["Name"]:Category(cat["Name"]) for cat in self.classes.values()}
        return cats