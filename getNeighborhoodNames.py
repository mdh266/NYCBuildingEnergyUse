import pandas as pd
from bs4 import BeautifulSoup
import requests

def main():
    """
    Function to get the neighborhood names of NYC from online website 
    using BeautifulSoup.
    """
    # url for zipcodes and neighborhoods
    url  = "https://www.health.ny.gov/statistics/cancer/registry/appendix/neighborhoods.htm"

    # get the html from the url
    site = requests.get(url)
    soup = BeautifulSoup(site.text,"lxml")

    # get the actual table and rows
    table = soup.find("table")
    rows  = table.find_all("td")[0:]

    # intialize the array of neighborhood
    neighborhoods_raw = []
    zipcodes_raw      = []

    # loop over the rows and collect the zip codes and 
    # associated neighborhood names
    for row in rows:
        if row.attrs['headers'][0] == 'header2':
            neighborhoods_raw.append(row.contents[0].strip())

        if row.attrs['headers'][0] == 'header3':
            zipcodes_raw.append(row.contents[0].strip())

    # now work on cleaning the zips and neighborhood
    neighborhoods = []
    zipcodes      = []

    # convert the zipcodes in to ints 
    # note: dont need to work about leading 0's 
    # since in NYC they start with 1's/
    for i in range(len(zipcodes_raw)):
        for zipcode in zipcodes_raw[i].split(","):
            zipcodes.append(int(zipcode))
            neighborhoods.append(neighborhoods_raw[i])

    # now turn it into the data into a pandas dataframe
    # and pickle it to use later.
    zip_df = pd.DataFrame({"postalCode": zipcodes, 
                           "PO_NAME"   : neighborhoods})

    zip_df.to_pickle("data/neighborhoods.pkl")


if "__name__" == "__main__":
    main()

