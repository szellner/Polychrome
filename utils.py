import re
import string
import cv2
import numpy as np
import utils
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def display_colors(colors):
    """Displays the suggested colors"""
    # initialize the bar chart representing the relative frequency
    # of each of the colors
    l = len(colors)
    h = 50
    w = l * 100

    bar = np.zeros((h, w, 3), dtype="uint8")
    startX = 0
    # loop over each color
    percent = l / 100.0
    for color in colors:
        endX = startX + 100
        array = np.array(utils.hex2rgb(color[1]))
        cv2.rectangle(bar, (int(startX), 0), (int(endX), h), array, -1)
        print startX, endX
        startX = endX
    gs = gridspec.GridSpec(1, 1)
    plt.figure(figsize=(20, 2))
    gs.update(left=0.02, right=0.98)
    ax = plt.subplot(gs[:5, :])
    plt.axis('off')
    ax.imshow(bar)
    plt.show()


def hex2rgb(hexVal):
    """Converts a hex value to an RGB value."""
    if hexVal.startswith('#'):
        hexVal = hexVal[1:]
    return tuple([int(hexVal[i:i + 2], 16) for i in xrange(0, len(hexVal), 2)])


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
