from solvers.solver import Solver


class AllInRowSolver(Solver):
    def __init__(self):
        pass

    def solve(self, event):
        categories = event.get_not_empty_categories_with_interval_start()
        schedule_length = sum([(cat.get_category_count() -1) * cat.min_interval + 1 for cat in categories.values()])
        schedule = [[] for _ in range(schedule_length)]
        act_time = 0
        for category in categories.values():
            category.final_interval = category.min_interval
            category.final_start = act_time
            for _ in range(category.get_category_count()):
                schedule[act_time].append(category.name)
                act_time += category.min_interval
            act_time -= category.min_interval
            act_time += 1
        return categories, schedule

    def get_name(self):
        return 'AllInRowSolver'
