import pandas as pd
import numpy as np
from get_data import get_data
from model import *
from onevsall import *
from ROC_report import *
from const import *
import os
import datarobot as dr


def pipeline():
    
    print(os.getcwd())
    print("Reading data")
    
    df = get_data()
    
    print("Project creation process started")
    dr.Client(token=DATAROBOT_API_TOKEN, endpoint=DATAROBOT_ENDPOINT)
    projects_list = build_onevsall(df = df, multiclass_column_name = multiclass_column_name)
    
    
    return projects_list





if __name__ == '__main__':
    print("Initiating")
    pipeline()