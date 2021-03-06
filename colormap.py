import re
import utils


class Colormap:
    def __init__(self, mapType, extras=False):
        self.mapType = mapType
        self.colors = {}
        with open("colormaps/{0}.txt".format(mapType)) as f:
            for line in f.readlines():
                # self.count +=1
                simpleMatch = re.search(
                    '([a-zA-Z0-9 \'\-\(\)\[\]]+)([0-9]+)? +(\#[a-zA-Z0-9]{6})', line)
                extrasMatch = re.search(
                    '([a-zA-Z \(\)]+) (\#[a-zA-Z0-9]{6}) ([a-zA-Z0-9 \*\#]+)?', line)
                nbsMatch = re.search(
                    '([a-zA-Z ]+) (\#[0-9A-Z]{6}) (\#[0-9A-Z]+) ([A-Za-z ]+) ?(\*OUT)? ?(\*IGNORE0)? ?(\*\#[0-9A-Z]+.+)?', line)

                if simpleMatch:
                    name, num, hexVal = simpleMatch.groups()
                    if num:
                        name = name + num
                    # If there are colors with the same hex but a different
                    # name, combine their dictionary values instead of
                    # replacing them
                    if hexVal in self.colors.keys():
                        self.colors[hexVal].append(name)
                    else:
                        self.colors[hexVal] = [name.strip()]
                # # elif extras and extrasMatch:
                # #     name, hexVal, extra = extrasMatch.groups()
                # #     self.colors[hexVal] = (name, extra)
                # # elif extras and nbsMatch:
                # #     if "OUT" not in nbsMatch.groups():
                # #         name, mundieHex, fosterHex, group = nbsMatch.groups()
                # #     else:
                # #         name, mundieHex, fosterHex, group, gamutException = nbsMatch.groups()
                # #     if "IGNORE0" not in nbsMatch.groups():
                # #         self.colors[mundieHex] = name
                # #     self.colors[fosterHex] = name
                # #     name, mundieHex, fosterHex, group, inGamut, = nbsMatch.groups()
                # else:
                #     if not line.startswith(';'):
                #         print "X ", line

    def toRGB(self):
        """Converts a Colormap"""
        newColors = {}
        for key, val in self.colors.items():
            if utils.validHex(key):
                key = utils.hex2rgb(key)
            newColors[key] = val
        self.colors = newColors
        return self

    def isMapType(self, requestedMapType):
        return self.mapType == requestedMapType
