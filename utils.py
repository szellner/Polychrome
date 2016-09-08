import re
import string
import cv2
import numpy as np
import webcolors

def display_colors(colors):
	"""Displays the suggested colors"""
	# initialize the bar chart representing the relative frequency
	# of each of the colors
	h = 50
	w = 400
	bar = np.zeros((h, w, 3), dtype = "uint8")
	startX = 0
	# loop over each color
	percent = len(colors)/100.0
	for color in colors:
		endX = startX + (percent * w)
		print color[1][1]
		col = color.astype("uint8").tolist()
		cv2.rectangle(bar, (int(startX), 0), (int(endX), h), col, -1)
		startX = endX
		colors.append(col)
	# return the bar chart
	print "BAR: ", bar
	print colors
	return bar, colors

def hex2rgb(hexVal):
    if hexVal.startswith('#'):
        hexVal = hexVal[1:]
    return tuple([int(hexVal[i:i + 2], 16) for i in xrange(0, len(hexVal), 2)])

def map2rgb(requested_map):
    	rgb = {}
    	for key, val in requested_map.items():
    		newKey = hex2rgb(key)
    		rgb[newKey] = val
        return rgb

def validHex(val):
	hexMatch = re.search('(\#)?([a-fA-F0-9]{6})', str(val))
	try:
		return '#' + hexMatch.groups()[1]
	except (AttributeError, TypeError):
		# print "%s is not a hex value." % val
		pass

def validRGB(val):
	try:
		len(val)==3 and val[0] in range(0,256) and val[1] in range(0,256) and val[2] in range(0,256)
		return val
	except AttributeError:
		# print "%s is not an RGB triplet." % str(val)
		pass

def manip():
	c= {}
	with open("xkcd.txt") as f:
		for line in f.readlines():
			match = re.search('([a-zA-Z ]+).(#[a-z0-9]+)', line)
			if match: 
				name, hexVal = match.groups()
				if ' ' in name:
					n = name.split()
					# print n
					if len(n)==3: 
						c[n[0]+n[1].title()+n[2].title()] = hexVal
						print n[0].title(),n[1].title(),n[2].title(), hexVal
					elif len(n)==2:
						c[n[0],n[1].title()] = hexVal
						print n[0].title(),n[1].title(), hexVal
					elif len(n)==1:
						print n[0].title(), hexVal
			
					

def m():
	with open("magick.txt") as f:
		for line in f.readlines():
			s = line.split()
			# print s
			get = re.findall('[A-Z][^A-Z]*', s[0])
			if get:
				match = re.search('([a-zA-Z ]+)([0-9]+)',s[0])
				if match:
					get2 = re.findall('[A-Z][^A-Z]*', match.groups()[0])
					if len(get2)==2:
						print get2[0], get2[1], match.groups()[1], s[1]
					if len(get2) == 3:
						print get2[0], get2[1], get2[2], match.groups()[1], s[1]
				else:
					print get[0], get[1],s[1]

			else:
				match = re.search('([a-zA-Z ]+)([0-9]+)',s[0])
				if match:
					print match.groups()[0].title(), match.groups()[1], s[1]
				else:
					print s[0].title(),s[1]
				# 	print match.groups()[0].title(), match.groups()[1], s[1]
				#  # src: http://www.imagemagick.org/script/color.php
	# if len(get)==2:
	# 				print get[0],get[1], s[1]
	# 			elif len(get)==3:
	# 				print get[0],get[1],get[2],s[1]
	# 		else:
			
def manip2():
	with open("magick.txt") as f:
		for line in f.readlines():
			if "#" in line:
				n,h = line.split()
				# print line.split()
				get = re.findall('[A-Z][^A-Z]*', n)
				if get:
					print get[0].lower()+get[1], h
					if len(get)==3:
						print get[0].lower()+get[1]+get[2], h
				else:
					print n, h
		
			# print n, h

def wiki(): 
	with open("wiki.txt") as f:
		for line in f.readlines():
			x = line.split()
			get = re.search('([a-zA-Z \(\)\/-\xc3]+).+(#[0-9A-Za-z]+)', line)
			if get:
				g = get.groups()
				print g[0], g[1] 
			# print x

def manip4():
	with open("resene.txt") as f:
		for line in f.readlines():
			if not line.startswith(';'):
				match = re.search('(Resene [a-zA-Z ]+).([0-9]+).([0-9]+).([0-9]+)', line)
				if match:
					name, r, g, b = match.groups()
					print name, '#%02x%02x%02x' % (int(r),int(g),int(b))

def manip5():
	with open("hollasch.txt") as f:
		for line in f.readlines():
			if not line.startswith("#"):
				split = line.split()
				name = split[0].split('_')
				n = [x.title() for x in name]
				if n[len(n)-1]=="Light" or n[len(n)-1]=="Deep" or n[len(n)-1]=="Medium" or n[len(n)-1]=="Pale" or n[len(n)-1]=="Dark":
					if len(n)==2:
						n = [n[len(n)-1], n[0]]
					if len(n)==3:
						n = [n[len(n)-1],n[0],n[1]]
				j = ' '.join(n)
				print j, "#"+split[1]
			else:
				print line


def checksatfaces():
	with open("satfaces.txt") as f:
		z = set()
		for line in f.readlines():
			z.add(line.split(']')[1].strip())
			
				# z.add(match.groups()[1])
				# if len(match)==3:
				# 	z.add(match.groups()[2])
		print z
def bang():
	with open("bang.txt") as f:
		for line in f.readlines():
			if not line.startswith(';'):
				match = re.search('([0-9]+).([0-9]+).([0-9]+).[0-9]+ ([a-zA-Z, ]+)',line)
				if match:
					g = match.groups()
					name = ' '.join([x.title() for x in g[len(g)-1].split()])
					print name, '#%02x%02x%02x' % (int(g[0]),int(g[1]),int(g[2]))

def ral(): 
	with open("ral.txt") as f:
		for line in f.readlines():
			s = line.split()
			hexval = s[1]
			name = ' '.join(x.title() for x in s[2:])
			print name, hexval, s[0]

def nbs():
	with open("nbs_iscc.txt") as f:
		for line in f.readlines():
			if not line.startswith(';') :
				s = line.split()
				n = [x.title() for x in s[0].split('_')]
				name = ' '.join(n)
				print name, s[1]

def cpant():
	with open("coatedPantone.txt") as f:
		for line in f.readlines():
			s = line.split()
			print ' '.join(s[0:len(s)-3])


def ntc(): 
	with open("ntc.txt") as f: 
		for line in f.readlines():
			s = line.split()
			h, n = s[0], s[1:]
			print ' '.join(n), '#'+h

def ntclvl3():
	with open("temp.txt") as f:
		for line in f.readlines():
			match = re.search('([a-z \.\-]+) \(([a-zA-Z \.]+)\)', line)
			if match:
				m = match.groups()[0].split()
				mj = ''.join([x.title() for x in m[1:]])
				# m = ''.join([x.title for x in match.groups()[0].split()[1:]])
				# print m
				print "def ", m[0]+mj, ":\n"
				print "    return ", match.groups()[0] ,",", match.groups()[1]

def camelCase(name):
	n = name.split()
	if len(n) == 1:
		return n[0]
	else:
		nUp = ''.join([x.title() for x in n[1:]])
		return n[0]+nUp

def ntclvl12():
	with open("temp.txt") as f:
		for line in f.readlines():
			match = re.search('([a-z ]+) \(([a-zA-Z]+)\)', line)
			if match:
				m = camelCase(match.groups()[0])
				print "def %s:\nif %s in name:\nreturn \"%s\"\n" % (m,match.groups()[1],match.groups()[0])


def nbs():
	with open("nbs.txt") as f:
		group = None
		for line in f.readlines():
			if not line.startswith(';'):
				if "GO TO TOP" in line:
					group = line.split("GO TO TOP")[0].strip()
				match = re.search('[a-zA-Z0-9 \-\.] [0-9]+ ([a-zA-Z ]+).+(\#[0-9A-Za-z]+).+(\#[0-9A-Za-z]+)', line)
				if match:
					print match.groups()[0], match.groups()[1], match.groups()[2], group

def weight(graph, node0, node1):
    	if not graph.has_edge(node0, node1):
            graph.add_edge(node0, node1, {"weight": 1})
        else:
            graph[node0][node1]["weight"] += 1
			
if __name__ == "__main__":   
	nbs()

	# # src: http://www.imagemagick.org/script/color.php
