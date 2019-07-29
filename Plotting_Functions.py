import pandas as pd
import matplotlib.pyplot as plt

from bokeh.plotting import figure
from bokeh.models import (
    GeoJSONDataSource,
    HoverTool,
    GMapPlot, GMapOptions, ColumnDataSource, 
    DataRange1d, PanTool, WheelZoomTool, BoxSelectTool,
    LogColorMapper,ColorBar
)
from bokeh.palettes import Plasma6 as palette

def plot_years_built(df : pd.DataFrame) -> None:
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
    
def make_interactive_choropleth_map(
    bokeh_source  : ColumnDataSource,
    count_var     : str,
    min_ct        : int,
    max_ct        : int
) -> figure:
    
    TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,save" 
    
    palette.reverse()
    
    color_mapper = LogColorMapper(palette=palette, 
                                  low=min_ct, 
                                  high=max_ct)
    
    fig = figure(title="{} By Zipcode".format(count_var), 
            tools=TOOLS,
            x_axis_location=None, 
            y_axis_location=None)  

    fig.grid.grid_line_color = None

    # Her is where we set the 
    fig.patches('x', 'y', 
                source=bokeh_source, 
                fill_color={'field':'counts',
                            'transform': color_mapper},
                fill_alpha=0.7, 
                line_color="white", 
                line_width=0.5)


    hover = fig.select_one(HoverTool)
    hover.point_policy = "follow_mouse"
    hover.tooltips = [("Neighborhood", "@PO_NAME"),
                      ("Zip Code", "@postalCode"),
                      (count_var, "@counts"),
                      ("(Long, Lat)", "($x, $y)")]

    # Add a color bar to understand the range of values the correspond to
    color_bar = ColorBar(color_mapper=color_mapper,
                         label_standoff=5, 
                         border_line_color=None, 
                         location=(0,0))

    fig.add_layout(color_bar, 'left')

    return fig