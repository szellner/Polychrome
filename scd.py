import re
import webcolors
import colorsys
from collections import defaultdict

class Polychrome2:
	def __init__(self):
		self.magickMap = self.createMap("magick")
		self.xkcdMap = self.createMap("xkcd")
		self.reseneMap = self.createMap("resene")
		self.bangMap = self.createMap("bang")
		self.hollaschMap = self.createMap("hollasch", True)
		self.ralMap = self.createMap("ral", True)
		self.nbsIsccMap = self.createMap("nbsiscc")
		self.wikiMap = self.createMap("wiki")
		self.coatedPantoneMap = self.createMap("coatedpantone")

	def createMap(self, mapType, extra=False):
		colorMap = {}
		with open(mapType+".txt") as f:
			for line in f.readlines():
				if extra:
					match = re.search('([a-zA-Z ]+) (#[a-zA-Z0-9]+) ([a-zA-Z0-9 ]+)?', line)
				else:
					match = re.search('([a-zA-Z0-9 ]+)([0-9]+)? +(#[a-zA-Z0-9]+)', line)
				if match:
					if extra:
						name, hexVal, extra = match.groups()
						colorMap[hexVal] = (name, extra)
					else:
						name, num, hexVal = match.groups()
						if num:
							colorMap[hexVal] = name+num
						else:
							colorMap[hexVal] = name.strip()
		return colorMap.items()

	def euclid(self, requested_color, key, name, store):
		r_c, g_c, b_c = webcolors.hex_to_rgb(key)
		rd = (r_c - requested_color[0]) ** 2
		gd = (g_c - requested_color[1]) ** 2
		bd = (b_c - requested_color[2]) ** 2
		store[(rd + gd + bd)] = name

	def closestColor(self, requested_color, requested_map, extra=False):
		min_colors = {}
		for key, name in requested_map:
			self.euclid(requested_color, key, name, min_colors)
		closest = min_colors[min(min_colors.keys())]
		if extra:
			return str(closest[0].title()), str(webcolors.normalize_hex(key)), str(closest[1].title())
		else:
			return str(closest.title()), str(webcolors.normalize_hex(key))

	def getWebName(self, requested_color, flag):
	 	try:
	 		if flag == "broad":
	 			colorName = webcolors.rgb_to_name(requested_color,spec="css21")
	 			hexVal = str(webcolors.css21_names_to_hex[colorName])
	 		elif flag == "specific":
	 			colorName = webcolors.rgb_to_name(requested_color,spec="css3")
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
		return self.closestColor(requested_color, self.hollaschMap, True)

	def getRalName(self, requested_color):
		return self.closestColor(requested_color, self.ralMap, True)
	
	def getNbsIsccName(self, requested_color):
		return self.closestColor(requested_color, self.nbsIsccMap)

	def getWikiName(self, requested_color):
		return self.closestColor(requested_color, self.wikiMap)

	def getCoatedPantoneName(self, requested_color):
		return self.closestColor(requested_color, self.coatedPantoneMap)

	def getSatName(self, requested_color):
		""" The dominant color name over the three fully-saturated faces of the RGB cube. From XKCD results. """
		r,g,b = map((lambda x: x/255.0),requested_color)
		(h, s, v) = colorsys.rgb_to_hsv(r, g, b)
		(r, g, b) = colorsys.hsv_to_rgb(h, 1, v)

		match = "[{}, {}, {}]".format(int(r*255.0), int(g*255.0), int(b*255.0))
		for line in open("satfaces.txt"):
		    if line.startswith(match):
		    	clean = line.split("] ")[1].strip()
		return clean

	def suggest(self, requested_color):
		suggestions = dict.fromkeys(["broadweb", "specweb", "magick", "xkcd", "resene", "bang", "nbsiscc" "pantone", "ral", "satfaces","chromaticity","munsell","wiki"])
		suggestions["broadweb"] = self.getWebName(requested_color,"broad")
		suggestions["specweb"] = self.getWebName(requested_color,"specific")
		suggestions["magick"] = self.getMagickName(requested_color)
		suggestions["xkcd"] = self.getXkcdName(requested_color)
		suggestions["resene"] = self.getReseneName(requested_color)
		suggestions["bang"] = self.getBangName(requested_color)
		suggestions["hollasch"] = self.getHollaschName(requested_color)
		suggestions["ral"] = self.getRalName(requested_color)
		suggestions["nbsiscc"] = self.getNbsIsccName(requested_color)
		suggestions["wiki"] = self.getWikiName(requested_color)
		suggestions["coatedpantone"] = self.getCoatedPantoneName(requested_color)
		suggestions["satfaces"] = self.getSatName(requested_color)

		for x in suggestions.items():
			if x[1]:
				print x

		

if __name__ == "__main__":    
	requested_color = (210,100,150)
	poly = Polychrome2()
	poly.suggest(requested_color)

