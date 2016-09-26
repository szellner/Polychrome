import colorsys
import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib import pyplot as plt
from matplotlib import gridspec
from colormap import Colormap
import utils
import textutils
from textwrap import wrap

# http://rgb.to/pantone
# Pantone Solid Coated
# 1761 colors
# Pantone Solid Uncoated
# 1761 colors
# Pantone Metallic
# 301 colors
# Pantone Pastels Neons Coated


class Polychrome:
    """"""
    def __init__(self):
        self.magickMap = Colormap("magick")
        self.xkcdMap = Colormap("xkcd")
        self.reseneMap = Colormap("resene")
        self.bangMap = Colormap("bang")
        self.hollaschMap = Colormap("hollasch", extras=True)
        self.ralMap = Colormap("ral", extras=True)
        self.nbsiscc1Map = Colormap("nbsiscc1")
        self.nbsiscc2Map = Colormap("nbsiscc2", extras=True)
        self.wikiMap = Colormap("wiki")
        self.coatedpantoneMap = Colormap("coatedpantone")
        self.ntcMap = Colormap("ntc")
        self.broadwebMap = Colormap("broadweb")
        self.specwebMap = Colormap("specweb")

        # Default is to convert all colormaps to RGB, since it makes
        # calculations significantly easier
        for key in self.__dict__:
            colormap = self.__dict__[key]
            colormap.toRGB()

    def isSupportedMap(self, mapType):
        """Checks the existing colormaps to see if the map type is supported."""
        name = mapType + "Map"
        try:
            return name in list(colormap[0] for colormap in self.__dict__.items())
        except KeyError:
            print "The map {0} isn't supported.".format(mapType)

    def getMap(self, mapType):
        """Gets a colormap by its keyname."""
        name = mapType + "Map"
        if self.isSupportedMap(mapType):
            return self.__dict__[name]
    
    def getMaps(self):
        """Gets all valid colormaps."""
        colormaps = []
        validMaps = list(key[:len(key) - 3] for key in self.__dict__.keys())
        for mapType in validMaps:
            colormaps.append(self.getMap(mapType))
        return colormaps

    def getMaps(self):
        """Gets all valid colormaps."""
        colormaps = []
        validMaps = list(key[:len(key) - 3] for key in self.__dict__.keys())
        for mapType in validMaps:
            colormaps.append(self.getMap(mapType))
        print len(colormaps)
        return colormaps

    def closestColor(self, requested_color, requested_map, compare="euclid", extras=False, intra=False):
        min_colors = {}
        if compare == "euclid":
            for key, name in requested_map.colors.items():
                utils.euclid(requested_color, key, name, min_colors)
            closestKey = min(min_colors.keys())
            if intra:
                min_colors.pop(closestKey)
                closestKey = min(min_colors.keys())
            closestName = min_colors[closestKey]
        # elif compare == "deltaE":
        #   self.deltaE()
        # Maps with simple extras

     #    if requested_map in ["hollaschMap", "ralMap"]:
        return closestKey[0], closestKey[1], closestName
     #    # Maps with complex extras
        # elif requested_map in ["inbsiscc_improvedMap"]:
     #            print "IS IMPR"


    def getSatName(self, requested_color):
        """ The dominant color name over the three fully-saturated faces of the RGB cube. From XKCD results."""
        r, g, b = map((lambda x: x / 255.0), requested_color)
        (h, s, v) = colorsys.rgb_to_hsv(r, g, b)
        (r, g, b) = colorsys.hsv_to_rgb(h, 1, v)

        match = "[{}, {}, {}]".format(
            int(r * 255.0), int(g * 255.0), int(b * 255.0))
        for line in open("colormaps/satfaces.txt"):
            if line.startswith(match):
                clean = line.split("] ")[1].strip()
        return clean

    def isInMap(self, requested_color, mapType):
        """Checks if a color is in a specific colormap."""
        try:
            colorMap = self.getMap(mapType)
            requested_color = utils.validColor(requested_color)
            return colorMap.colors[requested_color]
        except KeyError:
            print "The requested color {0} is not in the {1} map.".format(requested_color, mapType)
            pass

    def suggest(self, requested_color):
        """Suggests the closest named colors to the requested color. Gives one result for each valid colormap."""
        # Double check the requested color's validity
        requested_color = utils.validColor(requested_color)
        # Get the types of the valid maps
        validMaps = list(key[:len(key) - 3] for key in self.__dict__.keys())
        suggestions = dict.fromkeys(validMaps)
        for key in suggestions.keys():
            suggestions[key] = self.closestColor(
                requested_color, self.getMap(key))
        suggestions["satfaces"] = self.getSatName(requested_color)
        sortedKeys = sorted(suggestions, key=suggestions.__getitem__)
        print "REQUESTED COLOR: ", requested_color
        print "satfaces {0}".format(suggestions["satfaces"])
        sortedSuggestions = {}
        for key in range(1, len(suggestions)):
            colormap = sortedKeys[key]
            color = suggestions[colormap]
            sortedSuggestions[colormap] = color
            print "{0} {1} {2} {3} {4}".format(colormap, color[0], ', '.join(color[2]), color[1][0], color[1][1])
        print
        return suggestions, sortedKeys

    def display(self, requested_colors):
        for color in requested_colors:
            suggestions, sortedKeys = poly.suggest(color)
            l = len(sortedKeys) - 1
            w = l * 1.8
            suggw = (w / l) * 10
            fig = plt.figure(figsize=(w, 4))

            gsfig = gridspec.GridSpec(2, 1)
            # Gridspec for the required color subplots
            gsreq = gridspec.GridSpecFromSubplotSpec(
                2, l, subplot_spec=gsfig[0], height_ratios=[2, 1])
            reqRGB = utils.validColor(color)
            scaledReqRGB = list(x / 255.0 for x in reqRGB)
            # The requested color subplot
            ax1 = plt.subplot(gsreq[0, :], axisbg=scaledReqRGB)
            reqInfo = "{0}\n{1}".format(reqRGB, utils.rgb2hex(reqRGB))
            ax1.text(0.5, -0.4, reqInfo, ha="center", va="center")
            # Spacing accommodating text
            ax2 = plt.subplot(gsreq[1, :], frameon=False)
            axarr = [ax1, ax2]
            # The suggested colors subplot(s)
            gssugg = gridspec.GridSpecFromSubplotSpec(
                2, l, subplot_spec=gsfig[1], height_ratios=[2, 1])
            for i in range(1, l + 1):
                suggested_color = suggestions[sortedKeys[i]]
                scaledSuggRGB = list(x / 255.0 for x in suggested_color[1][0])
                name = ', '.join(suggested_color[2])
                wrappedName = '\n'.join(wrap(name, suggw))
                info = "{0}\n{1}\n{2}\n{3}".format(wrappedName, str(suggested_color[1][0]), suggested_color[1][
                                                   1], "dist: {0}".format(suggested_color[0]))
                suggax = plt.subplot(gssugg[0, i - 1], axisbg=scaledSuggRGB)
                suggax.set_title(sortedKeys[i], fontsize="small")
                suggax.text(0, -.1, info, fontsize="x-small", va="top")
                axarr.append(suggax)
            # More spacing accommodating text
            ax3 = plt.subplot(gssugg[1, :], frameon=False)
            axarr.append(ax3)

            # Make the axes labels and ticks invisible
            plt.setp([a.get_xaxis() for a in axarr[0:l + 3]], visible=False)
            plt.setp([a.get_yaxis() for a in axarr[0:l + 3]], visible=False)
            # Remove whitespace and show
            plt.tight_layout()
        plt.show()

    # def test_hsvSort(self,mapType):

    # def test_hilbertSort(self,mapType):
# def display2(self, requested_color):
#     suggestions, sortedKeys = poly.suggest(requested_color)


if __name__ == "__main__":

    requested_color = (20, 200, 107)
    requested_color2="#F70042"
    poly = Polychrome()
    cols = (requested_color, requested_color2)
#     # poly.isInMap((205, 200, 177), "wiki")
#     # poly.suggest(requested_color)
    poly.display(cols)
