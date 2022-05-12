import os.path

import pandas as pd
from os.path import isfile

LOG_PATH = os.path.join(os.path.dirname(__file__),'results/default_results.pkl')

class ResultLogger:
    def __init__(self, solver_name, result_file_name=LOG_PATH):
        self.data = {}
        self.data['solver_name'] = solver_name
        self.data['date'] = pd.Timestamp.now()
        self.result_filename = result_file_name

    def log_event(self, event, duration, schedule_length, was_valid):
        self.data[f'{event.id}'] = schedule_length
        #self.data[f'{event.id}_length'] = schedule_length
        self.data[f'{event.id}_duration'] = duration
        self.data[f'{event.id}_valid'] = was_valid
        pass

    def log_solver(self) ->str:
        log_in_pd = pd.DataFrame.from_dict({k:[v] for k,v in self.data.items()})
        if isfile(self.result_filename):
            old_logs = pd.read_pickle(self.result_filename)
            new_logs = pd.concat([old_logs, log_in_pd])
            new_logs.to_pickle(self.result_filename)
        else:
            log_in_pd.to_pickle(self.result_filename)
        return log_in_pd.to_string()
