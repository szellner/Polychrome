import colorsys
import utils
from colormap import ColorMap
import matplotlib as mpl 
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cv2
import numpy as np
# http://rgb.to/pantone
# Pantone Solid Coated
# 1761 colors
# Pantone Solid Uncoated
# 1761 colors
# Pantone Metallic
# 301 colors
# Pantone Pastels Neons Coated


class Polychrome:
    def __init__(self):
        self.magickMap = ColorMap("magick")
        self.xkcdMap = ColorMap("xkcd")
        self.reseneMap = ColorMap("resene")
        self.bangMap = ColorMap("bang")
        self.hollaschMap = ColorMap("hollasch", extras=True)
        self.ralMap = ColorMap("ral", extras=True)
        self.nbsiscc1Map = ColorMap("nbsiscc1")
        self.nbsiscc2Map = ColorMap("nbsiscc2", extras=True)
        self.wikiMap = ColorMap("wiki")
        self.coatedpantoneMap = ColorMap("coatedpantone")
        self.ntcMap = ColorMap("ntc")
        self.broadwebMap = ColorMap("broadweb")
        self.specwebMap = ColorMap("specweb")

    def euclid(self, requested_color, key, name, store):
        try:
            if utils.validHex(key):
                r_c, g_c, b_c = utils.hex2rgb(key)
            elif utils.validRGB(key):
                r_c, g_c, b_c = key
            rd = (r_c - requested_color[0]) ** 2
            gd = (g_c - requested_color[1]) ** 2
            bd = (b_c - requested_color[2]) ** 2
            store[(rd + gd + bd), key] = name
        except ValueError:
            pass

    def isSupportedMap(self, mapType):
        # Look whether the map type is supported
        name = mapType + "Map"
        return name in list(colormap[0] for colormap in self.__dict__.items())

    def getMap(self, mapType):
        name = mapType + "Map"
        try:
            return self.__dict__[name]
        except KeyError:
            print "The map %s isn't supported." % mapType

    def closestColor(self, requested_color, requested_map, compare="euclid", extras=False):
        min_colors = {}
        # If the requested color is in hex, change it to RGB
        if utils.validHex(requested_color):
            requested_color = utils.hex2rgb(requested_color)
        if utils.validRGB(requested_color):
            for key, name in requested_map.colors.items():
                self.euclid(requested_color, key, name, min_colors)
        closestKey = min(min_colors.keys())
        closestName = min_colors[closestKey]
        # if compare == "euclid":
        #   self.euclid(requested_color, key, name, min_colors)
        #   closest = min_colors[min(min_colors.keys())]
        # elif compare == "deltaE":
        #   self.deltaE()
        # Maps with simple extras

     #    if requested_map in ["hollaschMap", "ralMap"]:
        return closestKey[0], utils.validHex(closestKey[1]), closestName
     #    # Maps with complex extras
        # elif requested_map in ["inbsiscc_improvedMap"]:
     #            print "IS IMPR"

    def getSatName(self, requested_color):
        """ The dominant color name over the three fully-saturated faces of the RGB cube. From XKCD results. """
        if utils.validHex(requested_color):
            requested_color = utils.hex2rgb(requested_color)
        r, g, b = map((lambda x: x / 255.0), requested_color)
        (h, s, v) = colorsys.rgb_to_hsv(r, g, b)
        (r, g, b) = colorsys.hsv_to_rgb(h, 1, v)

        match = "[{}, {}, {}]".format(
            int(r * 255.0), int(g * 255.0), int(b * 255.0))
        for line in open("satfaces.txt"):
            if line.startswith(match):
                clean = line.split("] ")[1].strip()
        return clean

    def suggest(self, requested_color):
        # Get the types of the valid maps
        validMaps = list(key[:len(key) - 3] for key in self.__dict__.keys())
        suggestions = dict.fromkeys(validMaps)
        for key in suggestions.keys():
            suggestions[key] = self.closestColor(
                requested_color, self.getMap(key))
        suggestions["satfaces"] = self.getSatName(requested_color)
        sortedKeys = sorted(suggestions, key=suggestions.__getitem__)
        print "REQUESTED COLOR: ", requested_color
        for s in range(len(suggestions)):
            print sortedKeys[s], suggestions[sortedKeys[s]]
        print
        return suggestions

    def name(self, mapType, requested_color):
        colorMap = self.getMap(mapType)
        # For hex values
        if type(requested_color) == str:
            try:
                return colorMap.colors[utils.validHex(requested_color)]
            except KeyError:
                print "The hex value %s is not in the %s map." % (requested_color, mapType)
                pass
            except TypeError:
                pass
        # For RGB values
        elif type(requested_color) == tuple:
            try:
                rgbMap = colorMap.toRGB()
                return rgbMap.colors[utils.validRGB(requested_color)]
            except KeyError:
                print "The RGB triplet %s is not in the %s map." % (requested_color, mapType)
                pass
            except TypeError:
                pass

    def display(self, requested_color, suggestions):
        """Displays the suggested colors"""
        # Order named colors from the closest to the furthest away
        sortedKeys = sorted(suggestions, key=suggestions.__getitem__)
        # Set up basic variables to use
        l = len(suggestions)
        w = l * 100
        h = w / l
        percent = l / 100.0
        # Manages the subplots
        gs = gridspec.GridSpec(2, l)
        gridspec.GridSpec
        plt.figure(figsize=(20, 4))
        gs.update(left=0.02, right=0.98)
        # The suggested colors
        for i in range(1, l):
            bar = np.zeros((h, l + 100, 3), dtype="uint8")
            sugg = plt.subplot(gs[1, i])
            sortedSuggestions = suggestions[sortedKeys[i]]
            sugg.set_title(sortedKeys[i])
            array = np.array(utils.hex2rgb(sortedSuggestions[1]))
            cv2.rectangle(bar, (0, 0), (l + 100, l + 100), array, -1)
            sugg.axis('off')
            sugg.imshow(bar)
            # The text
            plt.text(0, h + 20, sortedSuggestions[2], wrap=True)
            plt.text(0, h + 40, "dist: %d" %
                     sortedSuggestions[0], wrap=True)

        # The requested color
        reqbar = np.zeros((h, l + 100, 3), dtype="uint8")
        req = plt.subplot(gs[0, :])
        req.set_title("REQUESTED")
        if utils.validHex(requested_color):
            array = np.array(utils.hex2rgb(requested_color))
        else:
            array = np.array(requested_color)
        cv2.rectangle(reqbar, (0, 0), (l + 100, l + 100), array, -1)
        req.axis('off')
        # plt.axis('off')
        req.imshow(reqbar)
        # for color in suggestions:
        #     endX = startX + 100
        #     array = np.array(utils.hex2rgb(color[1]))
        #     cv2.rectangle(bar, (int(startX), 0), (int(endX), h), array, -1)
        #     print startX, endX
        #     startX = endX

        plt.show()


if __name__ == "__main__":
    requested_color = (205, 200, 177)
    requested_color2 = "#003153"
    poly = Polychrome()
    # a = poly.suggest(requested_color)
    b = poly.suggest(requested_color2)
    poly.display(requested_color2, b)
