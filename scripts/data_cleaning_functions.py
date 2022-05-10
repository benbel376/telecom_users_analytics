import pandas as pd
import numpy as np

 
def fill_missing_by_mode(df, cols):
    """
    fills missing values by mode
    """
    mod_fill_list = []
    for i in range(cols.shape[0]):
        if(cols.iloc[i,3] == "object"):
            mod_fill_list.append(cols.iloc[i,0])
            
    for col in mod_fill_list:
        df[col] = df[col].fillna(df[col].mode()[0])
    return df


def fill_missing_by_mean(df, cols):
    """
    fills missing values by mean
    """
    mean_fill_list = []
    for i in range(cols.shape[0]):
        if(cols.iloc[i,3] == "float64"):
            mean_fill_list.append(cols.iloc[i,0])
    
    for col in mean_fill_list:
        df[col] = df[col].fillna(df[col].median())
    return df

def fill_missing_by_median(df, cols):
    """
    fills missing values by median.
    """
    median_fill_list = []

    for i in range(cols.shape[0]):
        if(cols.iloc[i,3] == "float64"):
            median_fill_list.append(cols.iloc[i,0])
            
    for col in median_fill_list:
        df[col] = df[col].fillna(df[col].median())
    return df


def fill_missing_forward(df, cols):
    """
    fills missing values by value from next rows
    """
    for col in cols:
        df[col] = df[col].fillna(method='ffill')
    return df

def fill_missing_backward(df, cols):
    """
    fills missing values by value from previous rows
    """
    for col in cols:
        df[col] = df[col].fillna(method='bfill')
    return df


def format_number(df, cols):
    """
    format floating number variables
    """
    float_format_list = []

    for i in range(cols.shape[0]):
        if(cols.iloc[i,3] == "float64"):
            float_format_list.append(cols.iloc[i,0])
    for col in float_format_list:
        df[col] = df.apply(lambda row : f'{row[col]:,.2f}', axis = 1)


    
    return df

