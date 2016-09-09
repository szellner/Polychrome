import re

def hex2rgb(hexVal):
    """Converts a hex value to an RGB value."""
    hexVal = validHex(hexVal)[1:]
    return tuple([int(hexVal[i:i + 2], 16) for i in xrange(0, len(hexVal), 2)])

def rgb2hex(rgbVal):
    """Converts an RGB value to a hex value."""
    rgbVal = validRGB(rgbVal)
    return '#%02x%02x%02x' % rgbVal

def map2rgb(requested_map):
    """Converts a dictionary/map of hex colors to a dictionary/map of RGB colors."""
    rgb = {}
    for key, val in requested_map.items():
        newKey = hex2rgb(key)
        rgb[newKey] = val
        return rgb


def validHex(val):
    """Checks if the given value is in valid hexadecimal format. Accepts values regardless of them having an octothorpe."""
    hexMatch = re.search('(\#)?([a-fA-F0-9]{6})', str(val))
    try:
        return '#' + hexMatch.groups()[1]
    except (AttributeError, TypeError):
        # print "%s is not a hex value." % val
        pass


def validRGB(val):
    """Checks if the given value is in valid RGB format."""
    try:
        len(val) == 3 and val[0] in range(0, 256) and val[
            1] in range(0, 256) and val[2] in range(0, 256)
        return val
    except AttributeError:
        # print "%s is not an RGB triplet." % str(val)
        pass


def weight(graph, node0, node1):
    """Adds new edges to or weights duplicate edges of a graph."""
    if not graph.has_edge(node0, node1):
        graph.add_edge(node0, node1, {"weight": 1})
    else:
        graph[node0][node1]["weight"] += 1
