import pandas as pd


def get_data():
    df = pd.read_csv("https://s3.amazonaws.com/datarobot_public_datasets/DR_Demo_Next_Best_Action.csv ")
    df.to_csv("data/raw/raw_Next_Best_Action.csv")
    df.to_csv("data/processed/processed_Next_Best_Action.csv")
    return df

