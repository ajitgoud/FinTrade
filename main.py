import os
from utils import load_yaml
from jobs import Compute
class FinTrade:
    def __init__(self):
        pass 
        
    def start(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        yaml_file = os.path.join(current_dir, 'configs', 'fintrade.yaml')
        config = load_yaml(yaml_file, as_namedtuple=True, base_dir=current_dir)
        Compute().start(config=config)
      
if __name__ == "__main__":
    trade = FinTrade()
    trade.start()