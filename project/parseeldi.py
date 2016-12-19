
class Ldi():
	def __init__(self, ldi):
		self.ldi=ldi
		self.location = getlocation(ldi) or []
		

		
def parseEldi(Eldi):
	eldi = Eldi.replace(' ','').split('#')
	observation = eldi[0]
	eldf = eldi[-1]
	return observation, eldf
	
def parseELDF(Eldf,operation):
	ldis = Eldf.split(operation)
	return ldis
