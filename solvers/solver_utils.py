from entity.category import Category
from entity.event import Event

def set_all_intervals_same(cats):
    max_interval = max([cat.min_interval for cat in cats.values()])
    for cat in cats.values():
        cat.min_interval = max_interval
    return max_interval, cats