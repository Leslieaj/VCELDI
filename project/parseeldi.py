
class Coefficientlocation:
	def __init__(self, coefficient, locationid):
		self.coefficient = coefficient
		self.location = locationid
		
class Ldi:
	def __init__(self, ldi):
		self.ldi=ldi
		self.coefficientlocations = getclocation(self.ldi) or []
		self.bound = getbound(self.ldi)
	def getbound(ldi):
		temp = ldi.split('<=')
		return temp[-1]
	def getclocation(ldi):
		temp = ldi.split('<=')
		cltemps = temp[0].split('+')
		clsequence = []
		for cl in cltemps:
			tempcl = cl.replace('[','').replace(']','').split(',')
			clsequence += [Coefficientlocation(tempcl[0],tempcl[-1])]
		

		
def parseEldi(Eldi):
	eldi = Eldi.replace(' ','').split('#')
	observation = eldi[0]
	eldf = eldi[-1]
	return observation, eldf
	
def parseELDF(Eldf,operation):
	ldis = Eldf.split(operation)
	return ldis
