import re
import webcolors
import colorsys
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
        self.magickMap = self.createMap("magick")
        self.xkcdMap = self.createMap("xkcd")
        self.reseneMap = self.createMap("resene")
        self.bangMap = self.createMap("bang")
        self.hollaschMap = self.createMap("hollasch", extras=True)
        self.ralMap = self.createMap("ral", extras=True)
        self.nbsIsccMap = self.createMap("nbsiscc")
        self.improvedNbsIsccMap = self.createMap(
            "nbsiscc_improved", extras=True)
        self.wikiMap = self.createMap("wiki")
        self.coatedPantoneMap = self.createMap("coatedpantone")
        self.ntcMap = self.createMap("ntc")

    def createMap(self, mapType, extras=False):
        colorMap = {}
        with open(mapType + ".txt") as f:
            for line in f.readlines():
                simpleMatch = re.search(
                    '([a-zA-Z0-9 \(\)\[\]]+)([0-9]+)? +(#[a-zA-Z0-9]+)', line)
                extrasMatch = re.search(
                    '([a-zA-Z \(\)]+) (#[a-zA-Z0-9]+) ([a-zA-Z0-9 \*\#]+)?', line)
                nbsMatch = re.search(
                    '([a-zA-Z ]+) (\#[0-9A-Z]+) (\#[0-9A-Z]+) ([A-Za-z ]+) ?(\*OUT)? ?(\*IGNORE0)? ?(\*\#[0-9A-Z]+.+)?', line)

                if simpleMatch:
                    name, num, hexVal = simpleMatch.groups()
                    if num:
                        colorMap[hexVal] = name + num
                    else:
                        colorMap[hexVal] = name.strip()
                elif extrasMatch:
                    name, hexVal, extra = extrasMatch.groups()
                    colorMap[hexVal] = (name, extra)
                elif nbsMatch:
                    if "OUT" not in nbsMatch.groups():
                        name, mundieHex, fosterHex, group = nbsMatch.groups()
                    else:
                        name, mundieHex, fosterHex, group, gamutException = nbsMatch.groups()
                    if "IGNORE0" not in nbsMatch.groups():
                        colorMap[mundieHex] = name
                    colorMap[fosterHex] = name
                    name, mundieHex, fosterHex, group, inGamut, = nbsMatch.groups()
                else:
                    if not line.startswith(';'):
                        print "X ", line

        return colorMap.items()

    def euclid(self, requested_color, key, name, store):
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        store[(rd + gd + bd)] = name

    # def deltaE(self, )

    def closestColor(self, requested_color, requested_map, compare="euclid", extras=False):
        min_colors = {}
        for key, name in requested_map:
            self.euclid(requested_color, key, name, min_colors)
            # if compare == "euclid":
            # 	self.euclid(requested_color, key, name, min_colors)
            # 	closest = min_colors[min(min_colors.keys())]
            # elif compare == "deltaE":
            # 	self.deltaE()
        closest = min_colors[min(min_colors.keys())]
        # Maps with simple extras
        if requested_map in ["hollaschMap", "ralMap"]:
            return str(closest[0]), str(webcolors.normalize_hex(key)), str(closest[1])
        # Maps with complex extras
        elif requested_map in ["improvedNbsIsccMap"]:
            print "IS IMPR"

        else:
            return str(closest.title()), str(webcolors.normalize_hex(key))

    # def getBroadWebName(self, requested_color, flag):
    #     try:
    #         colorName = webcolors.rgb_to_name(
    #             requested_color, spec="css21")
    #         hexVal = str(webcolors.css21_names_to_hex[colorName])
    #     except:
    #         webColorMap = webcolors.css21_hex_to_names.items()
    #         colorName = self.closestColor(requested_color, webColorMap)
    #         return colorName

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

    def getMagickName(self, requested_color):
        return self.closestColor(requested_color, self.magickMap)

    def getXkcdName(self, requested_color):
        return self.closestColor(requested_color, self.xkcdMap)

    def getReseneName(self, requested_color):
        return self.closestColor(requested_color, self.reseneMap)

    def getBangName(self, requested_color):
        return self.closestColor(requested_color, self.bangMap)

    def getHollaschName(self, requested_color):
        return self.closestColor(requested_color, self.hollaschMap)

    def getRalName(self, requested_color):
        return self.closestColor(requested_color, self.ralMap)

    def getNbsIsccName(self, requested_color):
        return self.closestColor(requested_color, self.nbsIsccMap)

    def getImprovedNbsIsccName(self, requested_color):
        return self.closestColor(requested_color, self.improvedNbsIsccMap)

    def getMunsellFosterName(self, requested_color):
        return self.closestColor(requested_color, self.nbsIsccMap)

    def getMunsellMundieName(self, requested_color):
        return self.closestColor(requested_color, self.nbsIsccMap)

    def getWikiName(self, requested_color):
        return self.closestColor(requested_color, self.wikiMap)

    def getCoatedPantoneName(self, requested_color):
        return self.closestColor(requested_color, self.coatedPantoneMap)

    def getNtcName(self, requested_color):
        return self.closestColor(requested_color, self.ntcMap)

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
        suggestions = dict.fromkeys(["broadweb", "specweb", "magick", "xkcd", "resene",
                                     "bang", "nbsiscc" "pantone", "ral", "satfaces", "chromaticity", "munsell", "wiki"])
        suggestions["broadweb"] = self.getWebName(requested_color, "broad")
        suggestions["specweb"] = self.getWebName(requested_color, "specific")
        suggestions["magick"] = self.getMagickName(requested_color)
        suggestions["xkcd"] = self.getXkcdName(requested_color)
        suggestions["resene"] = self.getReseneName(requested_color)
        suggestions["bang"] = self.getBangName(requested_color)
        suggestions["hollasch"] = self.getHollaschName(requested_color)
        suggestions["ral"] = self.getRalName(requested_color)
        suggestions["nbsiscc"] = self.getNbsIsccName(requested_color)
        suggestions["nbsiscc_improved"] = self.getImprovedNbsIsccName(
            requested_color)
        suggestions["wiki"] = self.getWikiName(requested_color)
        suggestions["coatedpantone"] = self.getCoatedPantoneName(
            requested_color)
        suggestions["ntc"] = self.getNtcName(requested_color)
        suggestions["satfaces"] = self.getSatName(requested_color)
        for x in suggestions.items():
            if x[1]:
                print x


if __name__ == "__main__":
    requested_color = (1,11,11)
    poly = Polychrome()
    poly.suggest(requested_color)
    
