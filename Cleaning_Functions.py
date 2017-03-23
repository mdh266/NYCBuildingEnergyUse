import pandas as pd
import re

def extract_string(string):
    """
    Removes some bad characters that get read in wrong.  
    It has to do with the ^2 in the columns names.

    :param: string (str):  string to strip

    :returns: The same string with any bad characters removed.
    :rtype: str
    """
    return str(re.sub('\xb2|\xc2\xb2','',string))


def initial_clean(df):
    """
    This function was mean to reduce all the dataframes from 2016-2012
    to have a consistent schema. It mostly renames the columns names
    and eliminates the columnst that are not consistent across the 
    years.
    
    :param: df (Pandas DataFrame): The Pandas DataFrame
    """
     # get rid of extra characters using extract sring
    columns = [extract_string(x) for x in list(df.columns)]
    df.columns = columns

    # Make dictionary to rename the column names
    column_names = {}
    column_names['Reported NYC Building Identification Numbers (BINs)'] = 'BINs'
    column_names['NYC Borough, Block and Lot (BBL)'] = 'BBL'
    column_names['Street Number'] = 'Street_Number'
    column_names['Street Name'] = 'Street_Name'
    column_names['Zip Code'] = 'Zip_Code'
    column_names['Borough'] = 'Borough'
    column_names['DOF Benchmarking Submission Status'] = 'Benchmarking_Status'
    column_names['Primary Property Type - Self Selected'] = 'Property_Type'
    column_names['Year Built'] = 'Year_Built'
    column_names['Site EUI (kBtu/ft)'] = 'Site_EUI'
    column_names['Natural Gas Use (kBtu)'] = 'Nat_Gas'
    column_names['Electricity Use - Grid Purchase (kBtu)'] = 'Elec_Use'
    column_names['Total GHG Emissions (Metric Tons CO2e)'] = 'GHG'
    column_names['ENERGY STAR Score'] = 'Energy_Star'
    column_names['Water Use (All Water Sources) (kgal)'] = 'Water_Use'
    column_names['Occupancy'] = 'Occupancy'

    # Now rename the columns names
    columns_to_drop = []
    for i in range(len(columns)):
        if columns[i] in column_names.keys():
            columns[i] = column_names[columns[i]]
        else:
            columns_to_drop.append(columns[i])
        
    new_df = df.copy()
    new_df.columns = columns
    
    new_df['Energy_Star'] = new_df['Energy_Star'].apply(clean_Energy_Star)
    new_df['Borough'] = new_df['Borough'].apply(clean_borough)
    new_df['Metered Areas (Energy)']
    new_df['NGI'] = new_df['Nat_Gas'] / new_df['DOF Property Floor Area (ft)']
    new_df['EI'] = new_df['Elec_Use'] / new_df['DOF Property Floor Area (ft)']
    new_df['WI'] = new_df['Water_Use'] / new_df['DOF Property Floor Area (ft)']
    
    
    #new_df.Zip_Code = new_df.Zip_Code.as_type(int)
    return new_df.drop(columns_to_drop, axis=1)
   
def group_property_types(row):
    """
    This functions changes each row in the dataframe to have the one
    of five options for building type:
    - Residential
    - Storage
    - Retail
    - Office
    - Other
    this was done to reduce the dimensionality down to the top building
    types.
    
    :param: row (str) : The row of the pandas series
    :rvalue: str
    :return: One of 5 building types.
    """
    if row == 'Multifamily Housing' or\
    row == 'Residence Hall/Dormitory' or\
    row =='Hotel' or\
    row == 'Other - Lodging/Residential' or\
    row == 'Residential Care Facility':
        return 'Residential'
    elif row == 'Non-Refrigerated Warehouse' or\
    row == 'Self-Storage Facility' or\
    row == 'Refrigerated Warehouse':
        return 'Storage'
    elif row == 'Financial Office' or\
    row == 'Office':
        return 'Office'
    elif row == 'Restaurant' or\
    row == 'Retail Store' or\
    row == 'Enclosed Mall' or\
    row == 'Other - Mall' or\
    row == 'Strip Mall' or\
    row == 'Personal Services (Health/Beauty, Dry Cleaning, etc.)' or\
    row == 'Lifestyle Center' or\
    row == 'Wholesale Club/Supercenter':
        return 'Retail'
    else:
        return 'Other'
    
def clean_Energy_Star(row):
    """
    This function is for converting the energy star rating in the
    dataframe from a string to a float.  We have to do use an 
    if else statement because some of the entries are actual string
    messages, so we return an nan for this case.
    
    
    :param: row (str): row in the the Pandas series
    :rvalue: int
    :returns: (str)
    """
    if row == 'Not Available'\
    or row == 'See Primary BBL':
        return float('nan')
    else:
        return float(row)
    
def clean_borough(row):
    """
    Removes the trailing space afer some boroughs.
    
    :param: row (str): row in the the Pandas series
    :rvalue: string
    :returns: removed trailing space from the row
    """
    if row == 'Manhattan ':
        return 'Manhattan'
    elif row == 'Brooklyn ':
        return 'Brooklyn'
    else:
        return row
    