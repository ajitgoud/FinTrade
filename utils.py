import os
import img2pdf
from datetime import date, timedelta

def generate_pdf(pdf_file, imgs_src):
    with open(pdf_file, "wb") as pdf:
        pdf.write(
            img2pdf.convert(
                [os.path.join(imgs_src, i) for i in os.listdir(imgs_src) if i.endswith(".png")])
            )

def remove_files(dir_path,ext=None):
    if not os.path.isdir(dir_path):
        if ext:
            os.remove(dir_path)
        else:
            print("Specify full path")
    else:
        for filename in os.listdir(dir_path):
            if filename.endswith(f'.{ext}'):
                os.remove(os.path.join(dir_path, filename))

def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def check_if_file_exists(dir_path):
    is_exist = os.path.exists(dir_path)
    if is_exist:
        print(f'{dir_path} exist.')
    else:
        print(f'{dir_path} does not exist.')
    return is_exist

def get_n_trading_days(days=None):
    day = date.today()
    count = days if days else 20
    dates = []
    while count > 0:
        if day.weekday() in [5,6]:
            day = day - timedelta(1)
        else:
            dates.append(day)
            day = day - timedelta(1)
            count-=1
    return dates

def get_working_day():
    day = date.today()
    while day.weekday() in [5,6]:
        day = day - timedelta(1)
    return day
