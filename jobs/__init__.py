from jobs.equity import Equity
from jobs.indices import Indices
from jobs.pnl import Pnl
from jobs.emas import Emas
class Compute:
    def __init__(self, **kwargs):
        pass
        
    def start(self, config):
        job_list = config.job_list
        common = config.common
        for job in job_list:
            eval(job.capitalize())().start(params=eval(f'config.jobs.{job}'), common=common)