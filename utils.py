import re
import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib import pyplot as plt

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

def weight(graph, node0, node1):
    """Adds new edges to or weights duplicate edges of a graph."""
    if not graph.has_edge(node0, node1):
        graph.add_edge(node0, node1, {"weight": 1})
    else:
        graph[node0][node1]["weight"] += 1
