from jobs.equity import Equity
from jobs.indices import Indices
class Compute:
    def __init__(self, **kwargs):
        pass
        
    def start(self, config):
        job_list = config.job_list
        common = config.common
        for job in job_list:
            if 'ind' in job:
                eval(job.capitalize())().start(params=eval(f'config.jobs.{job}'), common=common)
            