from entities.category import Category
from entities.athlete import Athlete
import json
from datetime import *

class Startlist_manager:
    def __init__(self, startlists_file):
        self.startlist = json.load(startlists_file)

    def get_schedule_length(self):
        min_date, max_date = self.__get_min_max_starttime()
        length = max_date - min_date
        return length.seconds // 60

    def get_schedule(self, cat_filter = None):
        min_date, max_date = self.__get_min_max_starttime()
        length = max_date - min_date
        schedule = [[] for _ in range((length.seconds // 60)+1)]
        for start in self.startlist.values():
            if cat_filter is not None and start['ClassDesc'] in cat_filter:
                start_date = datetime.strptime(start['StartTime'], '%Y-%m-%d %H:%M:%S')
                starttime = (start_date - min_date).seconds // 60
                schedule[starttime].append(start['ClassDesc'])
        return schedule


    def get_capacity(self, event):
        interval_cats = event.get_not_empty_categories_with_interval_start()
        schedule = {}
        for start in self.startlist.values():
            start_time = start['StartTime']
            start_cat = start["ClassDesc"]
            if start_cat in interval_cats:
                if start_time not in schedule:
                    schedule[start_time] = 1
                else:
                    schedule[start_time] += 1
        return max(schedule.values())

    def add_vacants(self, cats):
        for start in self.startlist.values():
            if start["Name"] in ['Vakant', 'Vakant ']:
                cats[start["ClassDesc"]].vacants_count += 1
        return cats

    def add_athletes(self, cats):
        for start in self.startlist.values():
            if start["Name"] not in ['Vakant', 'Vakant ']:
                cats[start["ClassDesc"]].athletes.append(Athlete(start['UserID'], start['ClubID']))
        return cats

    def __get_min_max_starttime(self):
        min_date = datetime.max
        max_date = datetime.min
        for start in self.startlist.values():
            date = datetime.strptime(start['StartTime'], '%Y-%m-%d %H:%M:%S')
            max_date = max(max_date, date)
            min_date = min(min_date, date)
        return min_date, max_date


