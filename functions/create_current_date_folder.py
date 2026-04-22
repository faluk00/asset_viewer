import os
from datetime import date

def create_current_date_folder(path):
    """
    Create a folder with the current date
    args
    path    str     dir path
    """
    today = date.today()
    today = today.strftime("%Y-%m-%d")
    if os.path.isfile(path):
        path, f = os.path.split(path)
    path = os.path.join(path, today)
    if not os.path.exists(path):
        os.makedirs(path)