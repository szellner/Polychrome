import webcolors
import colorsys
import utils
from colormap import ColorMap
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
        self.specwebMap = ColorMap("broadweb")

    def euclid(self, requested_color, key, name, store):
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        store[(rd + gd + bd)] = name

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
        if utils.validHex(str(requested_color)):
            requested_color = webcolors.hex_to_rgb(requested_color)
        # else:
        # 	print "OI", utils.validRGB(requested_color)
        if utils.validRGB(requested_color):
            for key, name in requested_map.colors.items():
                self.euclid(requested_color, key, name, min_colors)
                closest = min_colors[min(min_colors.keys())]
            # if compare == "euclid":
            # 	self.euclid(requested_color, key, name, min_colors)
            # 	closest = min_colors[min(min_colors.keys())]
            # elif compare == "deltaE":
            # 	self.deltaE()
            # Maps with simple extras

     #    if requested_map in ["hollaschMap", "ralMap"]:
        return closest, str(webcolors.normalize_hex(key))
     #    # Maps with complex extras
        # elif requested_map in ["inbsiscc_improvedMap"]:
     #            print "IS IMPR"
     #    else:
     #        return str(closest.title()), str(webcolors.normalize_hex(key))

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
        print "REQUESTED COLOR: ", requested_color
        for s in suggestions.items():
            print s
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

    def display(self, suggestions):
        print suggestions.values()
        print len(suggestions.values())
        suggestedColors = [
            val for val in suggestions.values() if type(val) == tuple]
        utils.display_colors(suggestedColors)

if __name__ == "__main__":
    requested_color = (205, 200, 177)
    requested_color2 = "#EE8262"
    poly = Polychrome()
    a = poly.suggest(requested_color)
    b = poly.suggest(requested_color2)
    poly.display(a)
