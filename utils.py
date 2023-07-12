# feature enginieering for timeseries with example call data X_train, y_train = create_features(pjme_train, target='PJME_MW')

def create_features(df, target=None):
    """
    Creates time series features from datetime index
    """
    df['date'] = df.index
    df['hour'] = df['date'].dt.hour
    df['dayofweek'] = df['date'].dt.dayofweek
    df['quarter'] = df['date'].dt.quarter
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['dayofyear'] = df['date'].dt.dayofyear
    df['dayofmonth'] = df['date'].dt.day
    df['weekofyear'] = df['date'].dt.weekofyear
    
    X = df[['hour','dayofweek','quarter','month','year',
           'dayofyear','dayofmonth','weekofyear']]
    if target:
        y = df[target]
        return X, y
    return X
# outlier report with example call -- outlier_report(ccm,vars_to_check,thres=4)

def outlier_report(df,vars_to_examine=None,color='red',thres=4,
                   return_df=False,no_print=False):
    '''
    Parameters
    ----------
    df : DATAFRAME
        Input dataframe
    vars_to_examine : LIST, optional
        List of variables to examine from dataframe. The default is df.columns.
    color : STRING, optional
        Color for cell highlighting. The default is 'red'.
    thres : int, optional
        Highlight cells where z score is above thres. The default is 4.
    return_df : Boolean, optional
        If true, will return the df obj (without styling) for further use. 
        The default is False.
    no_print : Boolean, optional
        If true, will not print. 
        The default is False.
    
    Displays (if no_print=False)
    -------
    Table with distribution of z-scores of variables of interest. 
    
    Returns (if return_df=True)
    -------
    Table with distribution of z-scores of variables of interest (without styling).     
    '''
        
    def highlight_extreme(s):
        '''
        Highlight extreme values in a series.
        '''
        is_extreme = abs(s) > thres
        return ['background-color: '+color if v else '' for v in is_extreme]
    
    if vars_to_examine==None:
        vars_to_examine=df.columns
    
    _tab = (
            # compute z scores
            ((df[vars_to_examine] - df[vars_to_examine].mean())/df[vars_to_examine].std())
            # output dist of z   
            .describe(percentiles=[.01,.05,.25,.5,.75,.95,.99]).T
            # add a new column = highest of min and max column
            .assign(max_z_abs = lambda x: x[['min','max']].abs().max(axis=1))
            # now sort on it
            .sort_values('max_z_abs',ascending = False)
    )
    
    if no_print == False:
        display(_tab
             .style.format('{:,.2f}')
                   .format({"count": '{:,.0f}'})           
                   .apply(highlight_extreme, 
                          subset=['mean', 'std', 'min', '1%', '5%', '25%', '50%', '75%', '95%','99%', 'max', 'max_z_abs'])
        ) 
    
    if return_df == True:
        return _tab
    
# Print missing and unique values in tabular format
from tabulate import tabulate
def tab_data(df):
    headers = ['Column', 'Null Count', 'Unique Count']
    meta_list = []
    cols = [i for i in df.columns]
    for col in cols:
        temp = []
        temp.append(col)
        temp.append(df[col].isna().sum())
        temp.append(df[col].nunique())
        meta_list.append(temp)
    print(tabulate(meta_list, headers, tablefmt='rst'))
    
# Segment the target variable by categorical features
import ipywidgets as widgets
from IPython.display import display
from IPython.display import clear_output
import seaborn as sns
import matplotlib.pyplot as plt

def segment_numeric_by_categoricals(df, categoricals, numeric, column_range=5, range_uniques=10, plot='boxplot'):
    column_ranges = list([categoricals[i:i+column_range] for i in range(0,len(categoricals),column_range)])
    print(column_ranges)
    for columns in column_ranges:
        for column in columns:
            #print(column)
            unique_values = df[column].unique()
            value_ranges = [unique_values[i:i+range_uniques] for i in range(0,len(unique_values),range_uniques)] 
            for value in value_ranges:
                #print(value)
                if plot == 'boxplot':
                    sns.boxplot(y=column, x=numeric, data=df[df[column].isin(value)])
                    plt.show()
                if plot == 'countplot':
                    sns.countplot(y=column, data=df[df[column].isin(value)])
                    plt.show()
                if plot == 'stats':
                    display(df[df[column].isin(value)].groupby(column).sum())
                    


                # Segment the target variable by categorical features
import ipywidgets as widgets

from IPython.display import display
from IPython.display import clear_output

# Dropdown for selecting columns and nr of samples with on change syncronised
def interactive_segment_numeric_by_categoricals(df):
    
    # define the widgets
    columns = widgets.SelectMultiple(
        options=df.select_dtypes(include='object').columns.values,
        description='Categoricals:',
        disabled=False,
    )

    column_range = widgets.IntText(
        value=5,
        description='Columns Range:',
        disabled=False
    )

    value_range = widgets.IntText(
        value=12,
        description='Uniques Values Range:',
        disabled=False
    )

    numeric = widgets.Dropdown(
        options=df.select_dtypes(include !='object').columns.values,
        description='Numerics:',
        disabled=False,
    )
    
    plot = widgets.Dropdown(
        options=['boxplot', 'countplot', 'stats'],
        description='Plot:',
        disabled=False,
    )

    # define the layout
    box_cat = widgets.VBox(children=[columns, column_range, value_range])
    box_num = widgets.VBox(children=[numeric, plot])
    box = widgets.HBox(children=[box_cat, box_num])

    out = widgets.Output()



    # define the action for value change
    def on_value_change(change):
        with out:
            clear_output()
            display(segment_numeric_by_categoricals(df,columns.value, numeric.value, column_range.value, value_range.value, plot.value))
        
    # define the listening for events
    columns.observe(on_value_change, names='value')
    column_range.observe(on_value_change, names='value')
    value_range.observe(on_value_change, names='value')
    numeric.observe(on_value_change, names='value')
    plot.observe(on_value_change, names='value')

    # display the initial state
    display(box, out)