"""
Project for Week 2 of "Python Data Visualization".
Read World Bank GDP data and create some basic XY plots.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import pygal


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table

def isfloat(string):
    """
    Takes a string as input and checks wether it can be converted to a float type
    """
    try:
        float(string)
        return True
    except ValueError:
        return False

def isint(string):
    """
    Takes a string as input and checks wether it can be converted to an int type
    """
    try:
        int(string)
        return True
    except ValueError:
        return False

def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output:
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """
    data = []
    minyear = gdpinfo["min_year"]
    maxyear = gdpinfo["max_year"]

    for year, gdp in gdpdata.items():
        year_isint = isint(year)
        gdp_isfloat = isfloat(gdp)
        if (year_isint) and (gdp_isfloat):
            gdp1 = float(gdp)
            year1 = int(year)
            if (gdp1 >= 0) and (maxyear >= year1 >= minyear):
                data.append((year1, gdp1))

    return data

def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values
      computed from the CSV file described by gdpinfo.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    plot_dict = {}

    #gdpdata_dict is a dict of dicts. The outer dict maps country name to the
    #row of that country. Inner dict maps column name to value
    gdpdata_dict = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_name"],
                                            gdpinfo["separator"], gdpinfo["quote"])

    #plot_dict is a dict that maps country to gdp_plot
    for country in country_list:
        if country in gdpdata_dict:
            #gdp_plot is a dict that maps year to gdp of the country specified
            gdp_plot = build_plot_values(gdpinfo, gdpdata_dict[country])
            gdp_plot.sort()
            plot_dict[country] = gdp_plot
        else:
            plot_dict[country] = []

    return plot_dict


def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None.

    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by gdpinfo for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """
    plot_dict = build_plot_dict(gdpinfo, country_list)

    gdp_chart = pygal.XY()
    gdp_chart.title = 'Plot of GDP for select countries spanning 1960 to 2015'
    gdp_chart.x_title = 'Year'
    gdp_chart.y_title= 'GDP in current US dollars'

    for country in country_list:
        gdp_chart.add(country, plot_dict[country])

    #gdp_chart.render_in_browser()
    gdp_chart.render_to_file(plot_file)


def test_render_xy_plot():
    """
    Code to exercise render_xy_plot and generate plots from
    actual GDP data.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    render_xy_plot(gdpinfo, [], "isp_gdp_xy_none.svg")
    render_xy_plot(gdpinfo, ["China"], "isp_gdp_xy_china.svg")
    render_xy_plot(gdpinfo, ["United Kingdom", "United States"],
                   "isp_gdp_xy_uk+usa.svg")


# Make sure the following call to test_render_xy_plot is commented out
# when submitting to OwlTest/CourseraTest.

#test_render_xy_plot()
