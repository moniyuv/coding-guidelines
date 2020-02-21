import datarobot as dr



def build_onevsall(df, multiclass_column_name):

    ## create a project per class for a one vs all type problem
    ## train an xgboost per project
    project_list = []
    classes = df[multiclass_column_name].unique()
    for c in classes:
        print("Building classification for "+c)
        df["target"] = df[multiclass_column_name].apply(lambda x: x == c)
        p = dr.Project.create(df.drop([multiclass_column_name],axis=1), project_name = c)
        p.set_target("target", mode="manual")
        blueprints = p.get_blueprints()
        model = list(filter(lambda x: "eXtreme" in str(x), blueprints)).pop(0)
        p.train(model, sample_pct=64)
        project_list.append(p)
        models = [p.get_models()[0] for p in project_list]
    return models
    
    

