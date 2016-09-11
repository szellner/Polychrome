import re
import colour
import colorsys
import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib import pyplot as plt

# Math
def euclid(requested_color, key, name, store):
    """Calculates the Euclidean distance between a requested color and a key color. Records the results in a given list store."""
    r_c, g_c, b_c = key
    rd = (r_c - requested_color[0]) ** 2
    gd = (g_c - requested_color[1]) ** 2
    bd = (b_c - requested_color[2]) ** 2
    store[(rd + gd + bd), (key, rgb2hex(key))] = name

# TODO
def hsvSort(colors):
    """Sort by HSV values."""
    data = []
    for count, color in colors:
        data.extend(count * [color])
    return data.sort()


def hilbertSort():
    """Sort using a Hilbert curve"""
    pass


def lumStep(r, g, b, repetitions=1):
    """Step sorting using hue and luminosity information"""
    lum = math.sqrt(.241 * r + .691 * g + .068 * b)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h2 = int(h * repetitions)
    lum2 = int(lum * repetitions)
    v2 = int(v * repetitions)
    return (h2, lum, v2)


def lumSort():
    colours.sort(key=lambda (r, g, b): step(r, g, b, 8))
# TODO

# Conversion functions
def hex2rgb(hexVal):
    """Converts a hex value to an RGB value."""
    try:
        hexVal = validHex(hexVal)
        return tuple([int(hexVal[i:i + 2], 16) for i in xrange(1, 7, 2)])
    except:
        print "Hex conversion to RGB has failed."


def rgb2hex(rgbVal):
    """Converts an RGB value to a hex value."""
    try:
        hexVal = '#%02x%02x%02x' % validRGB(rgbVal)
        return hexVal.upper()
    except:
        print "RGB conversion to hex has failed."

# Validity checkers
def validColor(val):
    if validHex(val):
        val = hex2rgb(val)
    try:
        return validRGB(val)
    except:
        print "{0} is not a valid color."


def validHex(val):
    """Checks if the given value is in valid hexadecimal format. Accepts values regardless of them having an octothorpe."""
    if type(val) == str:
        try:
            hexMatch = re.search('^(\#)?([a-fA-F0-9]{6})$', val)
            return '#' + hexMatch.groups()[1].upper()
        except:
            print "{0} is not a valid hex value.".format(val)


def validRGB(val):
    """Checks if the given value is in valid RGB format."""
    try:
        if type(val) == tuple and len(val) == 3 and all(val[i] in range(0, 256) for i in range(0, 3)):
            return val
    except:
        print "{0} is not a valid RGB value".format(val)
        pass


# Graph functions
def weight(graph, node0, node1):
    """Adds new edges to or weights duplicate edges of a graph."""
    if not graph.has_edge(node0, node1):
        graph.add_edge(node0, node1, {"weight": 1})
    else:
        graph[node0][node1]["weight"] += 1



