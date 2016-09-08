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

        self.mapDict = self.__dict__

    def euclid(self, requested_color, key, name, store):
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        store[(rd + gd + bd)] = name

    def isSupportedMap(self, mapType):
        # Look whether the map type is supported
        name = mapType + "Map"
        return name in list(colormap[0] for colormap in self.mapDict.items())

    def getMap(self, mapType):
        name = mapType + "Map"
        try:
            return self.mapDict[name]
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

            # print "RGB"
            # Maps with simple extras

     #    if requested_map in ["hollaschMap", "ralMap"]:
        return closest, str(webcolors.normalize_hex(key))
     #    # Maps with complex extras
        # elif requested_map in ["inbsiscc_improvedMap"]:
     #            print "IS IMPR"
     #    else:
     #        return str(closest.title()), str(webcolors.normalize_hex(key))

    def getWebName(self, requested_color, flag):
        try:
            if flag == "broad":
                colorName = webcolors.rgb_to_name(
                    requested_color, spec="css21")
                hexVal = str(webcolors.css21_names_to_hex[colorName])
            elif flag == "specific":
                colorName = webcolors.rgb_to_name(requested_color, spec="css3")
                hexVal = str(webcolors.css3_names_to_hex[colorName])
            return str(colorName).title(), hexVal
        except ValueError:
            if flag == "broad":
                webColorMap = webcolors.css21_hex_to_names.items()
            elif flag == "specific":
                webColorMap = webcolors.css3_hex_to_names.items()
            colorName = self.closestColor(requested_color, webColorMap)
            return colorName

    def getSatName(self, requested_color):
        """ The dominant color name over the three fully-saturated faces of the RGB cube. From XKCD results. """
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
        # suggestions = dict.fromkeys(["magick", "xkcd", "resene", "bang",
                                     # "nbsiscc1", "nbsiscc2", "coatedpantone", "ral", "wiki"])
        suggestions = dict.fromkeys(["magick"])
        for key in suggestions.keys():
            suggestions[key] = self.closestColor(
                requested_color, self.getMap(key))
        print "REQUESTED COLOR: ", requested_color
        for s in suggestions.items():
            print s
        print
# "broadweb", "specweb", "satfaces"

    def name(self, mapType, requested_color):
        colorMap = self.getMap(mapType)
        if type(requested_color) == str:
            try:
                return colorMap.colors[utils.validHex(requested_color)]
            except KeyError:
                print "The hex value %s is not in the %s map." % (requested_color, mapType)
                pass
            except TypeError:
                pass

        elif type(requested_color) == tuple:
            try:
                rgbMap = colorMap.toRGB()
                return rgbMap.colors[utils.validRGB(requested_color)]
            except KeyError:
                print "The RGB triplet %s is not in the %s map." % (requested_color, mapType)
                pass
            except TypeError:
                pass

if __name__ == "__main__":
    requested_color = (205, 200, 177)
    requested_color2 = "#EE8262"
    poly = Polychrome()
    # poly.name("magick", requested_color)
    # print poly.isSupportedMap("mgik")
    # print poly.isSupportedMap("magick")
    print poly.name("magick", requested_color2)
    print poly.name("magick", (205,201,201))
    print poly.name("magick", (40, 40, 40))
    # poly.suggest(requested_color)
    # poly.suggest(requested_color2)
