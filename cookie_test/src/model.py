import pandas as pd
import datarobot as dr
import time


def build_onevsall(df, multiclass_column_name):
    ## create a project per class for a one vs all type problem
    ## train an xgboost per project
    project_list = []
    classes = df[multiclass_column_name].unique()[:2]
    for c in classes:
        df["target"] = df[multiclass_column_name].apply(lambda x: x == c)
        print(f"Building project for {c} vs all")
        p = dr.Project.create(df.drop([multiclass_column_name],axis=1), project_name = c)
        p.set_target("target", mode="manual")
        blueprints = p.get_blueprints()
        model = list(filter(lambda x: "eXtreme" in str(x), blueprints)).pop(0)
        p.train(model, sample_pct=64)
        project_list.append(p)

    wait_for_jobs_to_complete(project_list)
    models = [p.get_models()[0] for p in project_list]
    return models

def wait_for_jobs_to_complete(project_list):
    
    jobs_list = []
    for p in project_list:
        jobs_list = jobs_list+p.get_all_jobs(dr.QUEUE_STATUS.INPROGRESS)
    
    num_jobs = len(jobs_list)    
    while num_jobs > 0:
        print (f"Waiting for remaining {num_jobs} jobs to finish")
        time.sleep(5 + (num_jobs) * 15)
        jobs_list = []
        for p in project_list:
            jobs_list = jobs_list+p.get_all_jobs(dr.QUEUE_STATUS.INPROGRESS)
        
        num_jobs = len(jobs_list) 
    print('All jobs complete!')