import pandas as pd
import numpy as np
from regex import D
from data_summarizing_functions import DataSummarizer;


class DataCleaner:
    """
    class that handles data cleaning.
    """
    def __init__(self) -> None:
        self.summar = DataSummarizer() 

    def remove_cols(self, df, cols, keep=False):
        """
        a functions that removes specified columns from dataframe
        """
        if(keep):
            r_df = df.loc[:,cols]
        else:
            r_df = df.drop(cols, axis=1)

        return r_df

    def reduce_dim_missing(self, df,limit):
        """
        removes columns with number of missing values greater than the provided limit
        """
        temp = self.summar.summ_columns(df)
        rem_lis = []
        for i in range(temp.shape[0]):
            if(temp.iloc[i,2] > limit):
                rem_lis.append(temp.iloc[i,0])
        r_df = df.drop(rem_lis, axis=1) 
        
        return r_df

    
    def fill_missing_by_mode(self, df, cols=None):
        """
        fills missing values by mode
        """
        mod_fill_list = []
        if(cols == None):
            temp = self.summar.summ_columns(df)
            for i in range(temp.shape[0]):
                if(temp.iloc[i,3] == "object"):
                    mod_fill_list.append(temp.iloc[i,0])
        else:
            for col in cols:
                mod_fill_list.append(col)
        
        for col in mod_fill_list:
            df[col] = df[col].fillna(df[col].mode()[0])
        
        return df


    def fill_missing_by_mean(self, df):
        """
        fills missing values by mean
        """
        temp = self.summar.summ_columns(df)
        mean_fill_list = []
        
        for i in range(temp.shape[0]):
            if(temp.iloc[i,3] == "float64"):
                mean_fill_list.append(temp.iloc[i,0])
        
        for col in mean_fill_list:
            df[col] = df[col].fillna(df[col].median())
        
        return df

    def fill_missing_by_median(self, df):
        """
        fills missing values by median.
        """
        temp = self.summar.summ_columns(df)
        median_fill_list = []

        for i in range(temp.shape[0]):
            if(temp.iloc[i,3] == "float64"):
                median_fill_list.append(temp.iloc[i,0])
                
        for col in median_fill_list:
            df[col] = df[col].fillna(df[col].median())
        return df


    def fill_missing_forward(self, df, cols):
        """
        fills missing values by value from next rows
        """
        for col in cols:
            df[col] = df[col].fillna(method='ffill')
        return df

    def fill_missing_backward(self, df, cols):
        """
        fills missing values by value from previous rows
        """
        for col in cols:
            df[col] = df[col].fillna(method='bfill')
        return df


    def format_number(self, df, cols):
        """
        format floating number variables
        """
        float_format_list = []

        for col in cols:
            float_format_list.append(col)
        for col in float_format_list:
            df[col] = df.apply(lambda row : f'{row[col]:,.2f}', axis = 1)

        return df


    def byte_to_mb(self, df, identifier):
        """
        converting byte to megabyte.
        """
        bytes_list = []
        megabyte = 1*10e+5
        temp = self.summar.summ_columns(df)
        
        for i in range(temp.shape[0]):
            if(identifier in temp.iloc[i,0]):
                bytes_list.append(temp.iloc[i,0])
        
        for col in bytes_list:
            df[col] = df[col]/megabyte
            df.rename(columns={col:col.replace(identifier,'(MB)')}, inplace=True)
        return df
