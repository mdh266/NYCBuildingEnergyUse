import pandas as pd
import geopandas as gpd
import re
from bokeh.plotting import ColumnDataSource
import numpy as np

def extract_string(string : str) -> str:
    """
    Removes some bad characters that get read in wrong.  
    It has to do with the ^2 in the columns names.

    :param: string (str):  string to strip

    :returns: The same string with any bad characters removed.
    :rtype: str
    """
    return str(re.sub('\xb2|\xc2\xb2','',string))

def compute_age(x : str) -> int:
    """
    Computes the age of the building.
    Somtimes the field contained string so I had to fill
    those as NULLs
    """
    if str(x).isdigit():
        return 2017 - x
    else:
        return np.nan
   

def initial_clean(df : pd.DataFrame) -> pd.DataFrame:
    """
    This function was mean to reduce all the dataframes from 2012-2016
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
    new_df['Borough']     = new_df['Borough'].apply(clean_borough)
    new_df['NGI']         = new_df['Nat_Gas'] / new_df['DOF Property Floor Area (ft)']
    new_df['EI']          = new_df['Elec_Use'] / new_df['DOF Property Floor Area (ft)']
    new_df['WI']          = new_df['Water_Use'] / new_df['DOF Property Floor Area (ft)']
    new_df['GHGI']        = new_df['GHG'] / new_df['DOF Property Floor Area (ft)']
    new_df['OPSFT']       = new_df['Occupancy'] / new_df['DOF Property Floor Area (ft)']
    new_df["Age"]         = new_df["Year_Built"].apply(compute_age)
    return new_df.drop(columns_to_drop, axis=1)


def group_property_types(row : str) -> str:
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
    row == 'Hotel' or\
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
    
def clean_Energy_Star(row : str) -> float:
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
    
def clean_borough(row : str) -> str:
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
    
    

def convert_GeoPandas_to_Bokeh_format(
    gdf : gpd.GeoDataFrame
) -> ColumnDataSource :
    """
    Function to convert a GeoPandas GeoDataFrame to a Bokeh
    ColumnDataSource object.
    
    :param: (GeoDataFrame) gdf: GeoPandas GeoDataFrame with polygon(s) under
                                the column name 'geometry.'
                                
    :return: ColumnDataSource for Bokeh.
    """
    gdf_new = gdf.drop('geometry', axis=1).copy()
    gdf_new['x'] = gdf.apply(getGeometryCoords, 
                             geom='geometry', 
                             coord_type='x', 
                             shape_type='polygon', 
                             axis=1)
    
    gdf_new['y'] = gdf.apply(getGeometryCoords, 
                             geom='geometry', 
                             coord_type='y', 
                             shape_type='polygon', 
                             axis=1)
    
    return ColumnDataSource(gdf_new)


def getGeometryCoords(
    row        : pd.Series,
    geom       : str,
    coord_type : str,
    shape_type : str
) -> float :
    """
    Returns the coordinates ('x' or 'y') of edges of a Polygon exterior.
    
    :param: (GeoPandas Series) row : The row of each of the GeoPandas DataFrame.
    :param: (str) geom : The column name.
    :param: (str) coord_type : Whether it's 'x' or 'y' coordinate.
    :param: (str) shape_type
    """
    
    # Parse the exterior of the coordinate
    if shape_type == 'polygon':
        exterior = row[geom].exterior
        if coord_type == 'x':
            # Get the x coordinates of the exterior
            return list( exterior.coords.xy[0] )    
        
        elif coord_type == 'y':
            # Get the y coordinates of the exterior
            return list( exterior.coords.xy[1] )

    elif shape_type == 'point':
        exterior = row[geom]
    
        if coord_type == 'x':
            # Get the x coordinates of the exterior
            return  exterior.coords.xy[0][0] 

        elif coord_type == 'y':
            # Get the y coordinates of the exterior
            return  exterior.coords.xy[1][0]
        