import pandas as pd
import matplotlib.pyplot as plt


def plot_years_built(df):
    """
    This function is used to plot the decade in which residential buildings 
    and office buildings were built. 
    
    :param: df (Pandas DataFrame) : The 2016 data after it is has been
                                    transformed to only have 5 different 
                                    property types by the function,
                                    group_property_types(...)
                                    
    """
    # Make the bins of decades since 1870
    bin_years = [1870 + 10*i for i in range(16)]
    
    fig = plt.figure(figsize=(10,5))
    
    plt.subplot(121)
    df[df['Property_Type'] == 'Multifamily Housing']\
    ['Year_Built'].value_counts(bins=bin_years).sort_index().plot(kind='bar',
                                     title='Year Multifamily Housing Built')
    plt.xlabel('Year')
    plt.ylim([0,2500])
    plt.ylabel('Count')
    
    
    plt.subplot(122)
    df[df['Property_Type'] == 'Office']\
    ['Year_Built'].value_counts(bins=bin_years).sort_index().plot(kind='bar',
                                      title='Year Office Built')
    plt.xlabel('Year')
    plt.ylim([0,2500])
    plt.ylabel('Count')
    
    plt.show()