import pandas as pd
import numpy as np

#filling missing values of categorical variables with mode 
def fill_missing_by_mode(df, cols):
    mod_fill_list = []
    for i in range(cols.shape[0]):
        if(cols.iloc[i,3] == "object"):
            mod_fill_list.append(cols.iloc[i,0])
            
    for col in mod_fill_list:
        df[col] = df[col].fillna(df[col].mode()[0])
    return df