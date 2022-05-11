import pandas as pd
from os.path import isfile

LOG_PATH ='results2.pkl'

class ResultLogger:
    def __init__(self, solver_name):
        self.data = {}
        self.data['solver_name'] = solver_name
        self.data['date'] = pd.Timestamp.now()

    def log_event(self, event, duration, schedule_length, was_valid):
        self.data[f'{event.id}'] = schedule_length
        #self.data[f'{event.id}_length'] = schedule_length
        self.data[f'{event.id}_duration'] = duration
        self.data[f'{event.id}_valid'] = was_valid
        pass

    def log_solver(self):
        log_in_pd = pd.DataFrame.from_dict({k:[v] for k,v in self.data.items()})
        if isfile(LOG_PATH):
            old_logs = pd.read_pickle(LOG_PATH)
            new_logs = pd.concat([old_logs, log_in_pd])
            new_logs.to_pickle(LOG_PATH)
        else:
            log_in_pd.to_pickle(LOG_PATH)

        pass
