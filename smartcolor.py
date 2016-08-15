# from collections import namedtuple, OrderedDict
# from colormath.color_objects import LabColor, sRGBColor

# class SmartColor:
# 	""" Descriptive colors.
# 		A modification of color_constants.py by Nat Dunn
# 	"""
# 	RGB = namedtuple('RGB', 'red, green, blue')
# 	LAB = namedtuple('LAB', 'lightness, a, b')

# 	def lab(self):
# 		""" Gets color in Lab format. """
# 		return "lab"
# 	def rgb(self):
# 		""" Gets color in rgb format. """
# 		return sRGBColor(self.red, self.green, self.blue)
# 	def bgr(self):
# 		""" Gets color in bgr format. """
# 		return (self.blue, self.green, self.red)
# 	def hex(self):
# 		""" Gets color in hex format. """
# 		return '#{:02X}{:02X}{:02X}'.format(self.red, self.green, self.blue)
# 	def human(self):
# 		""" Gets a color's name as humans would name it. """
# 		return "human"
# 	def web(self):
# 		""" Gets a color's name as is defined by web standards. """
# 		return "web" 
# 	def shade(self):
# 		""" Describes a color as light, bright, or dark. """
# 		return "shade"
# 	def simple(self): 
# 		""" Gives a very simple name to a given color. """
# 		return "simple"


# class SmartColorDict:
# 	""" Dictionary class for smart colors. """
	
# 	def useonly(self, colordict):
# 		""" Use only a specific dictionary for naming. """

# 	# def add_poi(self, lat, lon):
#  #    self.append(PoiData(lat, lon))
	
# 	# def add(self, SmartColor color):
# 		# """ Adds a color to the dictionary. """
# 		# what format is the color being added in 
# 		# what do you want to name this color

# 		return "add"
# 	def search(self):
# 		""" Searches the dictionary for a match. """
# 		return "search"
# 	def remove(self):
# 		""" Removes a color from the dictionary. """
# 		return "remove"


