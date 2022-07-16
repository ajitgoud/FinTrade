from jobs.equity import Equity
class Compute:
    def __init__(self, **kwargs):
        pass
        
    def start(self, config):
        job_list = config.job_list
        common = config.common
        for job in job_list:
           if 'eq' in job:
               eval(job.capitalize())().start(params=eval(f'config.jobs.{job}'), common=common)