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
            event.categories, schedule = self.solver.solve(event)
            end = time.time()
            solver_time = end - start
            if print_logs: print(f'Evaluation of event {event_id} finished with schedule length {len(schedule)}')
            if print_logs: print(f'Duration of solving was {solver_time}s')

            was_valid = Validator(schedule,event).validate_schedule()
            if print_logs & was_valid: print('Schedule is valid')
            if print_logs & (not was_valid): print('UNVALID')

            logger.log_event(event, solver_time,schedule, was_valid)

        logger.log_solver()
        if print_logs: print('Evaluation finished')