import pandas as pd
import numpy as np
import os

def download_data():
        
    df = pd.read_csv("https://s3.amazonaws.com/datarobot_public_datasets/DR_Demo_Next_Best_Action.csv")
    df.to_csv("data/raw/DR_Demo_Next_Best_Action.csv", index = False)
    
    return df