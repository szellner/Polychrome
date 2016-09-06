import re
import webcolors


class ColorMap:
    def __init__(self, mapType, extras=False):
        self.mapType = mapType
        self.colors = {}
        with open(self.mapType + ".txt") as f:
            for line in f.readlines():
                # self.count +=1
                simpleMatch = re.search(
                    '([a-zA-Z0-9 \(\)\[\]]+)([0-9]+)? +(#[a-zA-Z0-9]+)', line)
                extrasMatch = re.search(
                    '([a-zA-Z \(\)]+) (#[a-zA-Z0-9]+) ([a-zA-Z0-9 \*\#]+)?', line)
                nbsMatch = re.search(
                    '([a-zA-Z ]+) (\#[0-9A-Z]+) (\#[0-9A-Z]+) ([A-Za-z ]+) ?(\*OUT)? ?(\*IGNORE0)? ?(\*\#[0-9A-Z]+.+)?', line)

                if simpleMatch:
                    name, num, hexVal = simpleMatch.groups()
                    if num:
                        self.colors[hexVal] = name + num
                    else:
                        self.colors[hexVal] = name.strip()
                elif extras == True and extrasMatch:
                    name, hexVal, extra = extrasMatch.groups()
                    self.colors[hexVal] = (name, extra)
                elif extras == True and nbsMatch:
                    if "OUT" not in nbsMatch.groups():
                        name, mundieHex, fosterHex, group = nbsMatch.groups()
                    else:
                        name, mundieHex, fosterHex, group, gamutException = nbsMatch.groups()
                    if "IGNORE0" not in nbsMatch.groups():
                        self.colors[mundieHex] = name
                    self.colors[fosterHex] = name
                    name, mundieHex, fosterHex, group, inGamut, = nbsMatch.groups()
                else:
                    if not line.startswith(';'):
                        print "X ", line
    # def toRGB(self):
    # 	for x in colors:
    # 		print "X: ", x
            # print utils.hex2rgb()

    def displayMap(self):
        print "display"

    def isMapType(self, requestedMapType):
    	return self.mapType == requestedMapType
    	
    def name(self, hexVal):
        try:
        	return self.colors[hexVal]
        except KeyError:
        	print "This color doesn't exist in the %s map. Try again!" % self.mapType
