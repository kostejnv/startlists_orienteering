from solvers.solver import Solver
from solvers.solver_utils import set_all_intervals_to_power_2
import copy
from math import log2, ceil
from categories_modificators.courses_joiner import CoursesJoiner


class BestIntervalChooser(Solver):
    '''
    this chooser try all possible same intervals for categories

    for given power of two set all min_interval same - at lower interval
    increase interval, at bigger increase number of atheletes
    '''

    def __init__(self, solver):
        '''

        :param solver: solver that process modificated categories
        '''
        self.solver = solver
        self.__original_vacants = {} #internal variable used in __return_cats_back_acc_to_ratio
        pass

    def solve(self, event):
        proc_event = copy.deepcopy(event)

        categories = proc_event.get_not_empty_categories_with_interval_start()
        categories = set_all_intervals_to_power_2(categories)
        cs = CoursesJoiner(list(categories.values()))
        categories =  cs.join()

        max_interval = max([cat.min_interval for cat in categories.values()])
        all_intervals = [2 ** i for i in range(int(log2(max_interval)) + 1)]

        min_schedule_length = max([cat.get_category_count() for cat in categories.values()]) * max_interval * len(categories) # upper bound for schedule
        best_cats = {}
        for act_interval in all_intervals:
            ratios = self.__get_ratios_for_given_interval(act_interval, categories)
            cats_w_gvn_interval = self.__get_categories_with_given_ratio(copy.deepcopy(categories), ratios)

            proc_event.categories = cats_w_gvn_interval
            solved_cats, schedule_length = self.solver.solve(proc_event)

            if schedule_length < min_schedule_length:
                best_cats = self.__return_cats_back_acc_to_ratio(solved_cats, ratios)
                min_schedule_length = schedule_length

        return cs.disjoin(list(best_cats.values())), min_schedule_length

    def get_name(self):
        return f'BestIntervalChooser with {self.solver.get_name()}'

    def __get_ratios_for_given_interval(self, interval, cats):
        '''
        original interval 8, actual interval 2 -> ratio 4
        :param interval:
        :param cats:
        :return: ratios for each category how much interval is decrease
        '''
        ratios = {}
        for cat in cats.values():
            ratios[cat.name] = ceil(cat.min_interval/interval)
        return ratios

    def __get_categories_with_given_ratio(self, cats, ratios):
        '''
        change categories acc to ratio
        :param cats: categories to change
        :param ratios: decreasing ratio ber=tween original and actual ratio
        :return: changed categories
        '''
        self.__original_vacants = {}
        for cat in cats.values():
            if cat.name in ratios:
                cat.min_interval = cat.min_interval // ratios[cat.name]
                self.__original_vacants[cat.name] = cat.vacants_count
                cat.vacants_count += (cat.get_category_count() -1) * ratios[cat.name] + 1 - cat.get_category_count()
            else:
                raise f"Internal error: cat {cat.name} not in ratios"
        return cats

    def __return_cats_back_acc_to_ratio(self, solved_cats, ratios):
        '''
        return category back to original interval and number of athletes
        :param solved_cats: proccessed categories with given ratio
        :param ratios: ratios of the categories
        :return: categories with original number of athletes
        '''
        for cat in solved_cats.values():
            if cat.name in ratios:
                cat.final_interval = cat.final_interval * ratios[cat.name]
                cat.vacants_count = self.__original_vacants[cat.name]
            else:
                raise f"Internal error: cat {cat.name} not in ratios"
        return solved_cats
