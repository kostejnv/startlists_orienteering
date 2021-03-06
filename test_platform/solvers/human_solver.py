import os.path

from test_platform.solvers.solver import Solver
from test_platform.input_manager.startlists_manager import Startlist_manager


class HumanSolver(Solver):
    def __init__(self):
        self.script_dir = os.path.dirname(__file__)

    def solve(self, event):
        categories = event.get_not_empty_categories_with_interval_start()
        startlist_path = os.path.join(self.script_dir, f"../data/{event.id}/startlists.json")
        with open(startlist_path) as f:
            schedule = Startlist_manager(f).get_schedule(cat_filter=categories.keys())

        for cat_name, cat_data in categories.items():
            cat_starttimes = (idx for idx, cats in enumerate(schedule) if cat_name in cats)
            cat_start = next(cat_starttimes)
            cat_interval = next(cat_starttimes, cat_start) - cat_start
            if cat_interval != 0:
                cat_data.final_interval = cat_interval
            cat_data.final_start = cat_start

        return categories, len(schedule)

    def get_name(self):
        return 'RealStartlists'
