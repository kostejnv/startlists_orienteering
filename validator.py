import numpy as np
from collections import Counter

class Validator:
    def __init__(self, schedule, event):
        self.schedule = schedule
        self.event = event

    def validate_schedule(self):
        if (
                self.__validate_first_control() and
                self.__contains_all_categories() and
                self.__validate_cat_intervals_and_length() and
                self.__validate_capacity() and
                self.__validate_far_and_near_cat()

        ):
            return True
        else:
            return False

    def __contains_all_categories(self):
        # check if categories has start_time and interval
        interval_cats = self.event.get_not_empty_categories_with_interval_start()
        for cat_name, cat_data in interval_cats.items():
            if (cat_data.final_interval is None) or (cat_data.final_start is None):
                print(f'SOLVER ERROR! Category {cat_name} does not fill in final start and interval')
                return False

        reshape_schedule = [cat for minute in self.schedule for cat in minute]
        cat_set = set(reshape_schedule)
        for cat_name, cat_data in interval_cats.items():
            if (cat_data.get_category_count()) > 0 and (cat_name not in cat_set):
                print(f'SOLVER ERROR! Category {cat_name} is not in schedule')
                return False

        return True

    def __validate_capacity(self):
        if any(map(lambda x: len(x) > self.event.capacity, self.schedule)):
            print(f'SOLVER ERROR! Capacity constraint was not satisfied')
            return False
        return True

    def __validate_cat_intervals_and_length(self):
        interval_cats = self.event.get_not_empty_categories_with_interval_start()
        for cat_name, cat_data in interval_cats.items():
            if cat_data.final_interval == 0:
                print('000')
            for i in range(cat_data.final_start, cat_data.final_interval * cat_data.get_category_count(),
                           cat_data.final_interval):
                if i < len(self.schedule) and cat_name not in self.schedule[i]:
                    print(f'SOLVER ERROR! There should be {cat_name} at the time {i} in the schedule')
                    return False
        return True

    def __validate_first_control(self):
        first_control_schedule = [list(map(lambda cat: self.event.categories[cat].first_control, minute))for minute in self.schedule]
        failing_minutes = 0
        for minute, controls_in_minute in enumerate(first_control_schedule):
            if len(controls_in_minute) == 0: continue
            most_common_control, number_of_occurences = Counter(controls_in_minute).most_common(1)[0]
            if number_of_occurences > 1:
                print(f'SOLVER ERROR! In the time {minute} there are more runners with control {most_common_control}')
                #return False
                failing_minutes +=1
        print(f'{failing_minutes} start time failed from {len(first_control_schedule)}')
        if failing_minutes < 1:
            return True
        return False

    def __validate_far_and_near_cat(self):
        return True
