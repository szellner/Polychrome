import scd
import re

class PolychromeTests():
	
	def __init__(self):
		self.polychrome = scd.Polychrome()
		self.magickMap = self.polychrome.createMap("magick")
		# self.xkcdMap = self.createMap("xkcd")
		# self.reseneMap = self.createMap("resene")
		# self.bangMap = self.createMap("bang")
		# self.hollaschMap = self.createMap("hollasch", extras=True)
		# self.ralMap = self.createMap("ral", extras=True)
		self.nbsIsccMap = self.polychrome.createMap("nbsiscc")
		self.improvedNbsIsccMap = self.polychrome.createMap("nbsiscc_improved", extras=True)
		# self.wikiMap = self.createMap("wiki")
		# self.coatedPantoneMap = self.createMap("coatedpantone")
		# self.ntcMap = self.createMap("ntc")
		self.swm_count = 0
		self.swm_correlate = []
		self.nbs_count = 0
		self.nbs_correlate = []
		self.total = 0
		
		
	def specWebAndMagickEquivalence(self, test_color):
		magick = self.polychrome.getMagickName(test_color)
		msplit = magick[0].split()
		match = re.search('([a-zA-Z]+) ([0-9]+)', magick[0])
		if match:
			magick = ''.join([x.lower() for x in msplit[:len(msplit)-1]])
		else:
			magick = ''.join([x.lower() for x in magick[0].split()])
		specweb = self.polychrome.getWebName(test_color,"specific")[0].lower()
		if specweb == magick:
			self.swm_count += 1
		else:
			if (specweb,magick) not in self.swm_correlate and (magick,specweb) not in self.swm_correlate:
				self.swm_correlate.append((specweb,magick))
		self.total += 1
			
	def nbsAndImprovedEquivalence(self, test_color):
		nbs = self.polychrome.getNbsIsccName(test_color)[0]
		nbs_improved = self.polychrome.getImprovedNbsIsccName(test_color)[0]
		if nbs == nbs_improved:
			self.nbs_count += 1
		else:
			if (nbs,nbs_improved) not in self.nbs_correlate and (nbs, nbs_improved) not in self.nbs_correlate:
				self.nbs_correlate.append((nbs, nbs_improved))
		self.total += 1
			




if __name__ == "__main__":
	ptest = PolychromeTests()
	for r in range(1,65,10):
		for g in range(1,65,10):
			for b in range(1,65,10):
	# for r in range(1,256,10):
	# 	for g in range(1,256,10):
	# 		for b in range(1,256,10):
				rgb = (r, g, b)
				ptest.specWebAndMagickEquivalence(rgb)
				ptest.nbsAndImprovedEquivalence(rgb)

	print "specweb&magick %d / %d" % (ptest.swm_count, ptest.total)
	print "nbs&improved %d / %d" % (ptest.nbs_count, ptest.total)
	# for item in ptest.nbs_correlate:
	# 	print item