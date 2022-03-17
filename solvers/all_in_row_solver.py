from solvers.solver import Solver


class AllInRowSolver(Solver):
    def __init__(self):
        pass

    def solve(self, event):
        categories = event.get_not_empty_categories_with_interval_start()
        max_interval = max([cat.min_interval for cat in categories.values()])
        schedule_length = sum([(cat.get_category_count() -1) * cat.min_interval + 1 for cat in categories.values()]) + (len(categories) - 1) * (max_interval-1)
        schedule = [[] for _ in range(schedule_length)]
        act_time = 0
        for category in categories.values():
            category.final_interval = category.min_interval
            category.final_start = act_time
            for _ in range(category.get_category_count()):
                schedule[act_time].append(category.name)
                act_time += category.min_interval
            act_time -= category.min_interval
            act_time += max_interval
        return categories, schedule_length

    def get_name(self):
        return 'AllInRowSolver'
