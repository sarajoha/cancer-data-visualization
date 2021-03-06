"""
Week 1 practice project template for Python Data Visualization
Load a county-level PNG map of the USA and draw it using matplotlib
"""

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib as mpl
import math
import csv

# Houston location

USA_SVG_SIZE = [555, 352]
HOUSTON_POS = [270, 260]

def compute_county_cirle(county_population):
    """
    Takes a number as an input, that represents the population of a county
    and return a scaled number so it can be taken as the point size for a
    scatter plot
    """

    rescaled = county_population / 10000
    return rescaled

def create_riskmap(colormap=mpl.cm.jet):
    """
     Takes a colormap from the module matplotlib.cm module and returns a
     function that maps a cancer risk to an RGB value from the given colormap.
    """
    #norm = colors.LogNorm(vmin=table[-1][4], vmax=table[0][4])
    #norm = colors.LogNorm()
    #scalar = sm(norm=norm, cmap=cm.jet)
    #rbg = sm.to_rgba()

    return lambda x: mpl.cm.ScalarMappable(norm=colors.LogNorm(vmin=min(x), vmax=max(x)),
                                            cmap=colormap).to_rgba(x)


def draw_USA_map(map_name, table):
    """
    Given the name of a PNG map of the USA (specified as a string),
    draw this map using matplotlib
    """

    # Load map image, note that using 'rb'option in open() is critical since png files are binary
    with open(map_name, 'rb') as read_map:
        map = plt.imread(read_map)

    #  Get dimensions of USA map image
    ypixels, xpixels, bands = map.shape

    # Plot USA map
    map_image = plt.imshow(map)

    #Make lists of the data to plot
    cancer_risk = [float(row[4]) for row in table]
    x_coords = [(float(row[5]) * xpixels) / USA_SVG_SIZE[0] for row in table]
    y_coords = [(float(row[6]) * ypixels) / USA_SVG_SIZE[1] for row in table]
    population = [compute_county_cirle(int(row[3])) for row in table]

    #plot data in a scatter plot
    cmap = create_riskmap()
    plt.scatter(x = x_coords, y = y_coords, s=population, c=cmap(cancer_risk))

    plt.show()
    #plt.savefig("map.png")


#draw_USA_map("USA_Counties_555x352.png")
#draw_USA_map("USA_Counties_1000x634.png")

def read_csv_file(file_name):
    """
    Given a CSV file, read the data into a nested list
    Input: String corresponding to comma-separated  CSV file
    Output: Nested list consisting of the fields in the CSV file
    """

    with open(file_name, newline='') as csv_file:       # don't need to explicitly close the file now
        csv_table = []
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            csv_table.append(row)
    return csv_table


def draw_cancer_risk_map(joined_csv_file_name,map_name,num_counties=0):
    """
     Takes the name of a CSV file and the name of the USA map and draws a scatter plot
      with scatter points of fixed size and color at the center of the num_counties
      counties with highest cancer risk.
      Omitting the final optional argument num_counties
      should default to drawing all counties.
    """

    csv_file = read_csv_file(joined_csv_file_name)

    #sort table by cancer risk
    csv_file.sort(key=lambda row: float(row[4]), reverse=True)

    #plot map
    if num_counties != 0:
        trim_table = csv_file[0:num_counties]
        map = draw_USA_map(map_name, trim_table)
    else:
        map = draw_USA_map(map_name, csv_file)

#tests
#draw_cancer_risk_map("cancer_risk_joined.csv","USA_Counties_1000x634.png", 20)
#draw_cancer_risk_map("cancer_risk_joined.csv","USA_Counties_1000x634.png", 100)
draw_cancer_risk_map("cancer_risk_joined.csv","USA_Counties_1000x634.png")
