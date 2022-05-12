from test_platform.input_manager.input_manager import Input_manager
from test_platform.validator import Validator
from test_platform.logger import ResultLogger
import os

from os import listdir
import time

class Evaluator:
    def __init__(self, solver, solver_name):
        self.solver = solver
        self.solver_name = solver_name
        self.script_dir = os.path.dirname(__file__)

    def evaluate_solver(self, verbose=True):
        if verbose: print('Evaluation begins...')
        logger = ResultLogger(self.solver.get_name())
        data_path =os.path.join(self.script_dir, "data")
        event_ids = [item for item in listdir(data_path) if item.isnumeric()]
        for event_id in event_ids:
            if verbose: print('-----------------------------------------')
            event = Input_manager(event_id).get_event()
            if verbose: print(f'Evaluation of event {event_id} begins...')
            start = time.time()
            individual_cats, schedule_length = self.solver.solve(event)
            event = self.__merge_solved_cats_to_event(individual_cats, event)
            end = time.time()
            solver_time = end - start

            was_valid = Validator(event, schedule_length).validate_schedule()
            if verbose & was_valid: print('Schedule is valid')
            if verbose & (not was_valid): print('UNVALID')

            if verbose: print(f'Evaluation of event {event_id} finished with schedule length {schedule_length}')
            if verbose: print(f'Duration of solving was {solver_time}s')

            logger.log_event(event, solver_time,schedule_length, was_valid)

        results = logger.log_solver()
        print('_________________________________________________________')
        print(results)
        if verbose: print('Evaluation finished')

    def __merge_solved_cats_to_event(self, ind_cats, event):
        for cat in ind_cats.values():
            event.categories[cat.name] = cat
        return event