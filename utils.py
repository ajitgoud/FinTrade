from ast import pattern
import os
import json
import yaml
import re
from datetime import date, timedelta, datetime
from collections import namedtuple
from numpy import number

def remove_files(dir_path,subs=None, ext=None):
    print(f'Dir path: {dir_path} Subs: {subs} Ext: {ext}')
    if subs and isinstance(subs, list):
        for sub in subs:
            path = os.path.join(dir_path, sub)
            for filename in os.listdir(path):
                if filename.endswith(f'.{ext}'):
                    os.remove(os.path.join(path, filename))
    elif os.path.isdir(dir_path):
        if ext:
            for filename in os.listdir(dir_path):
                if filename.endswith(f'.{ext}'):
                    os.remove(os.path.join(dir_path, filename))
        else:
            print("Specify full path")
    else:
        print(dir_path)

def make_dirs(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def create_dir(dir_path, subs=None):
    if subs and isinstance(subs, list):
        make_dirs(dir_path)
        for sub in subs:
            make_dirs(os.path.join(dir_path, sub))
    else:
        make_dirs(dir_path)

def check_if_file_exists(dir_path):
    is_exist = os.path.exists(dir_path)
    if not is_exist:
        print(f'{dir_path} does not exist.')
    return is_exist

def get_n_trading_days(days=None):
    now = datetime.now()
    day = now.date()
    holidays = get_holidays()    
    month = day.strftime("%b").upper()
    if now.hour < 18:
        day = day - timedelta(1)
    count = days if days else 20
    dates = []
    while count > 0:
        if day.weekday() in [5,6] or day.day in holidays.get(str(day.year)).get(month) :
            day = day - timedelta(1)
        else:
            dates.append(day)
            day = day - timedelta(1)
            count-=1
        month = day.strftime("%b").upper()
    return dates

def get_working_day():
    holidays = get_holidays()
    now = datetime.now()
    day = now.date()
    month = day.strftime("%b").upper()
    if now.hour < 18:
        day = day - timedelta(1)

    while day.weekday() in [5,6] or day.day in holidays.get(str(day.year)).get(month):
        day = day - timedelta(1)
    return day

def get_holidays():
    holiday_file = "holiday.json"
    holiday_file_dir = os.path.dirname(os.path.realpath(__file__))
    holiday_file = os.path.join(holiday_file_dir, "configs", holiday_file)
    with open(holiday_file, "r") as days:
        holidays = json.load(days)
    return holidays

def mean(data, n = None):
    if isinstance(data, number) and n:
        mean = round(data / n, 2)
    else:
        n = len(data)
        mean = sum(data) / n
    return round(mean,2)

def get_n_trading_weeks(days=None):
    now = datetime.now()
    day = now.date()
    holidays = get_holidays()    
    month = day.strftime("%b").upper()
    if now.hour < 18:
        day = day - timedelta(1)
    count = days if days else 20
    weeks=[]
    dates = []
    while count > 0:
        if day.weekday() in [5,6]:
            day = day - timedelta(1)            
        else:
            if not day.day in holidays.get(str(day.year)).get(month):
                dates.append(day)
            if day.weekday() == 0:
                weeks.append(dates)
                dates=[]
            day = day - timedelta(1)
            count-=1
        month = day.strftime("%b").upper()
    return weeks

def variance(data):
    n = len(data)
    m = mean(data)
    deviations = [(x - m) ** 2 for x in data]
    variance = sum(deviations) / n
    return round(variance,2)

def stdev(data):
    import math
    var = variance(data)
    std_dev = math.sqrt(var)
    return round(std_dev,2)

def replace(res, common):
    if '/' in res and not 'url' in res:
        res = res.split('/')
        res = os.path.join(*res)
    pattern = re.compile(r'(<([\w]+)>)')
    result = re.findall(pattern, res)
    for key in result:
        res = res.replace(key[0], common[key[1]])
    return res

def update_config(config):
    pattern = re.compile(r'(<([\w]+)>)')
    for key, value in config.items():
        if isinstance(value, dict):
            for k, v in value.items():
                if not v:
                    pass
                elif isinstance(v, dict):
                    for i, j in v.items():
                        if not j:
                            pass
                        elif isinstance(j, dict):
                            for m, n in j.items():
                                if not n:
                                    pass
                                elif isinstance(n, dict):
                                    print(n)
                                elif isinstance(n, list):
                                    pass
                                else:
                                    n = str(n)
                                    res = re.search(pattern, n)
                                    if res:
                                        config[key][k][i][m] = replace(n, config['common'])

                        elif isinstance(j, list):
                            pass
                        else:
                            print(j)
                            res = re.search(pattern, j)
                            if res:
                                config[key][k][i] = replace(j, config['common'])
                    
                elif isinstance(v, list):
                    pass
                else:
                    print(v)
                    res = re.search(pattern, v)
                    if res:
                        config[key][k] = replace(v, config['common'])

        elif isinstance(value, list):
            print('list')
        else:
            print('mere')
    return config

def load_yaml(yaml_file, **kwargs):
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)
        today = get_working_day()
        config['common']['dd'] = today.strftime("%d")
        config['common']['mm'] = today.strftime("%m")
        config['common']['mm_str'] = today.strftime("%b").upper()
        config['common']['yyyy'] = str(today.year)
        config['common']['weekday'] = str(today.weekday())
        if kwargs.get('base_dir'):
            config['common']['base_dir'] = kwargs.get('base_dir')
        config = update_config(config)
        if kwargs.get('as_namedtuple'):
            return convert_to_namedtuple(config)
        return config

def convert_to_namedtuple(dictionary):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            dictionary[key] = convert_to_namedtuple(value)
    return namedtuple('configuration', dictionary.keys())(**dictionary)