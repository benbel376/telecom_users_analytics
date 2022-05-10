import pandas as pd
import numpy as np
from pandasql import sqldf
import matplotlib.pyplot as plt
import seaborn as sns

class DataSummarizer:
    """
    a class with list of data sumarizing methods.
    """
    def __init__(self) -> None:
        pass
    
    
    def sum_columns(self, df):
        """
        shows columns and their missing values along with data types.
        """
        df2 = df.isna().sum().to_frame().reset_index()
        df2.rename(columns = {'index':'variables', 0:'missing_count'}, inplace = True)
        df2['missing_percent_(%)'] = round(df2['count']*100/df.shape[0])
        data_type_lis = df.dtypes.to_frame().reset_index()
        df2['data_type'] = data_type_lis.iloc[:,1]
        
        unique_val = []
        for i in range(df2.shape[0]):
            unique_val.append(len(pd.unique(df[df2.iloc[i,0]])))
        df2['unique_values'] = pd.Series(unique_val)
        return df2


    def get_top_n(self, df, colname, num, globalDict):
        """
        a function that groups a column and return the top n groups based on member count
        """
        queryDf = lambda q: sqldf(q, globalDict)
        query = 'SELECT "'+colname+'", count(*) as user_count FROM '+df+' WHERE "'+colname+'" != "undefined" group by "'+colname+'" order by user_count DESC LIMIT '+str(num)
        return queryDf(query)


    def manByHandset(self, lis, dfname, globalDict):
        """
        a function that returns top three handsets from top three manufacturers
        """
        queryDf = lambda q: sqldf(q, globalDict)
        for man in lis:
            query = 'SELECT "Handset Manufacturer", "Handset Type", count(*) as num_users \
            FROM '+dfname+'\
            WHERE "Handset Manufacturer" = "'+man+'" \
            group by "Handset Type" \
            order by num_users DESC \
            LIMIT 3'
            print(queryDf(query),'\n')


    def find_agg(self, df, group_columns, agg_columns, agg_metrics, new_columns):
        """
        a function that returns a new dataframe with aggregate values of specified columns.
        """
        new_column_dict ={}
        agg_dict = {}
        for i in range(len(agg_columns)):
            new_column_dict[agg_columns[i]] = new_columns[i]
            agg_dict[agg_columns[i]] = agg_metrics[i]

        new_df = df.groupby(group_columns).agg(agg_dict).reset_index().rename(columns=new_column_dict)
        return new_df


    def combineColumns(self, df, col1, col2, new_name, rem=False):
        """
        combines two numerical variables and create new variable.
        """
        df[new_name] = df[col1]+df[col2]
        if(rem):
            df.drop([col1, col2], axis = 1, inplace = True)


    def generateFreqTable(self, df, cols, range):
        """
        generate a freqeuncy table
        """
        for col in cols:
            print(df[col].value_counts().iloc[:range,])


    def summary_one(self, df, cols):
        """
        calculate range, max, count, and min.
        """
        df2 = df[cols]
        
        df_sum = df2.max().to_frame().reset_index().rename(columns={"index":"variables",0:"max"})
        df_sum["min"] = df2.min().to_frame().reset_index().iloc[:,1]
        df_sum['range'] = df_sum['max'] - df_sum['min']
        df_sum["count"] = df2.count().to_frame().reset_index().iloc[:,1]
        return df_sum


    def summary_two(self, df, cols):
        """
        calculate central tendency measures.
        """
        df2 = df[cols]
        df_sum = df2.mean().to_frame().reset_index().rename(columns={"index":"variables",0:"mean"})
        df_sum["median"] = df2.median().to_frame().reset_index().iloc[:,1]
        df_sum["mode"] = df2.mode().iloc[:,1]
        return df_sum


    def summary_three(self, df, cols):
        """
        calculate dispersion measures
        """
        df2 = df[cols]
        df_sum = df2.std().to_frame().reset_index().rename(columns={"index":"variables",0:"std"})
        df_sum["var"] = df2.var().to_frame().reset_index().iloc[:,1]
        return df_sum


    def bar_graph(self, df, cols, x_ax):
        """
        graphical univariate analysis function. bar chart.
        """
        plot_df = df[cols]
        plt.figure(figsize=(25, 12))
        sns.countplot(x= x_ax, data=plot_df)


    def bivariateAnalysis(self, df, col , cols, crosst=False):
        """
        scatter plot and cross tab drawer
        """
        for col2 in cols:
            df_plot = df[[col2, col]]
            sns.relplot(data=df_plot, aspect = 2.0)
            if(crosst):
                pd.crosstab(df[col2], df[col], margins=True)


    def topDecile(self, df, group, cols, metric, name, top=5):
        """
        function that aggregates based on top n deciles.
        """
        aggr_n = self.find_agg(df, group, cols, metric, name)
        aggr_n = aggr_n.loc[aggr_n['Decile'] < top+1]
        return aggr_n


    def corrMatrix(self, df, cols):
        """
        a function that generates correlation matrix as a table.
        """
        relation = df[cols].corr()
        return relation