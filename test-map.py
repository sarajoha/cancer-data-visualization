"""
Week 1 practice project template for Python Data Visualization
Load a county-level PNG map of the USA and draw it using matplotlib
"""

import matplotlib.pyplot as plt

# Houston location

USA_SVG_SIZE = [555, 352]
HOUSTON_POS = [270, 260]

def draw_USA_map(map_name):
    """
    Given the name of a PNG map of the USA (specified as a string),
    draw this map using matplotlib
    """

    # Load map image, note that using 'rb'option in open() is critical since png files are binary
    with open(map_name, 'rb') as read_map:
        map = plt.imread(read_map)

    #  Get dimensions of USA map image
    ypixels, xpixels, bands = map.shape
    #print(xpixels, ypixels, bands)

    # Plot USA map
    map_image = plt.imshow(map)

    # Plot green scatter point in center of map
    plt.scatter(x = xpixels/2, y = ypixels/2, c='green')
    #iterates through the table and scatters x and y coordinates
    for row in table:
        x_coord = float(row[5])
        y_coord = float(row[6])
        x_resize = (x_coord * xpixels) / USA_SVG_SIZE[0] #reescale for larger png
        y_resize = (y_coord * ypixels) / USA_SVG_SIZE[1]
        plt.scatter(x = x_resize, y = y_resize, s=1, c='blue')

    # Plot red scatter point on Houston, Tx - include code that rescale coordinates for larger PNG files
    x_resize = (HOUSTON_POS[0] * xpixels) / USA_SVG_SIZE[0]
    y_resize = (HOUSTON_POS[1] * ypixels) / USA_SVG_SIZE[1]
    plt.scatter(x = x_resize, y = y_resize, s = 100, c='red')
    plt.show()


#draw_USA_map("USA_Counties_555x352.png")
draw_USA_map("USA_Counties_1000x634.png")
