import pandas as pd
import numpy as np
from download_data import download_data
from model import *
from onevsall import *
from ROC_report import *
from const import *
import os


def pipeline():
    print(os.getcwd())
    df = download_data()
    
    dr.Client(token=DATAROBOT_API_TOKEN, endpoint=DATAROBOT_ENDPOINT)
    projects_list = build_onevsall(df = df, multiclass_column_name = multiclass_column_name)
    
    
    return projects_list





if __name__ == '__main__':
    print("Initiating")
    pipeline()