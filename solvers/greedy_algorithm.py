from solvers.solver import Solver
from categories_modificators.courses_joiner import CoursesJoiner


def first_possible_minute(cat, schedule, capacity):
    for minute, controls in enumerate(schedule):
        if len(controls) < capacity and cat.first_control not in controls:
            return minute



class GreedySolver(Solver):
    def __init__(self):
        pass

    def solve(self, event):
        categories = event.get_not_empty_categories_with_interval_start()
        cs = CoursesJoiner(list(categories.values()))
        categories = cs.join()
        interval = max([cat.min_interval for cat in categories.values()])
        # initialisation
        opt_upper_bound = sum([cat.min_interval * cat.get_category_count() for cat in categories.values()])
        res = [[] for _ in range(opt_upper_bound)]
        for cat in categories.values():
            cat.final_interval = interval
        for cat in categories.values():
            cat.final_start = first_possible_minute(cat, res, event.capacity)
            for j in range(cat.get_category_count()):
                idx = cat.final_start + j * interval
                res[idx].append(cat.first_control)
        c_max = max([i+1 for i in range(len(res)) if res[i]])
        return cs.disjoin(list(categories.values())), c_max

    def get_name(self):
        return 'GreedySolver'