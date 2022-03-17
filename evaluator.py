from input_manager.input_manager import Input_manager
from validator import Validator
from logger import ResultLogger

from os import listdir
import time

class Evaluator:
    def __init__(self, solver, solver_name):
        self.solver = solver
        self.solver_name = solver_name

    def evaluate_solver(self, print_logs=True):
        if print_logs: print('Evaluation begins...')
        logger = ResultLogger(self.solver.get_name())
        event_ids = listdir('data')
        for event_id in event_ids:
            if print_logs: print('-----------------------------------------')
            event = Input_manager(event_id).get_event()
            if print_logs: print(f'Evaluation of event {event_id} begins...')
            start = time.time()
            individual_cats, schedule_length = self.solver.solve(event)
            event = self.__merge_solved_cats_to_event(individual_cats, event)
            end = time.time()
            solver_time = end - start

            was_valid = Validator(event, schedule_length).validate_schedule()
            if print_logs & was_valid: print('Schedule is valid')
            if print_logs & (not was_valid): print('UNVALID')

            if print_logs: print(f'Evaluation of event {event_id} finished with schedule length {schedule_length}')
            if print_logs: print(f'Duration of solving was {solver_time}s')

            logger.log_event(event, solver_time,schedule_length, was_valid)

        logger.log_solver()
        if print_logs: print('Evaluation finished')

    def __merge_solved_cats_to_event(self, ind_cats, event):
        for cat in ind_cats.values():
            event.categories[cat.name] = cat
        return event