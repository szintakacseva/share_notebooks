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
        options=df.select_dtypes(include='float64').columns.values,
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