from entity.category import Category
from entity.athlete import Athlete
import json

class Entries_manager:
    def __init__(self, entries_file):
        self.entries = json.load(entries_file)

    def add_athletes_info_to_cats(self, cats):
        for entry in self.entries.values():
            cat_name = entry['ClassDesc']
            athlete = Athlete(entry['UserID'],entry['ClubID'])
            cats[cat_name].athletes.append(athlete)
        return cats

