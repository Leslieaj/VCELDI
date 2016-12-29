
class Coefficientlocation:
	def __init__(self, coefficient, locationid):
		self.coefficient = coefficient
		self.location = locationid
		self.dvalue = []
	def adddvalue(self, dvaluestr):
		self.dvalue.append(dvaluestr)
	def getdvalue(self):
		if len(self.dvalue) == 0:
			return None
		temp = ''
		for i, dvaluestr in zip(range(0,len(self.dvalue)), self.dvalue):
			if i != len(self.dvalue) - 1:
				temp = temp + dvaluestr + '+'
			else:
				temp = temp + dvaluestr
		return temp
	def getcodvalue(self):
		if len(self.dvalue) == 0:
			return None
		temp = self.getdvalue()
		return '('+self.coefficient+')' + '*'+'('+temp+')'

class Ldi:
	def __init__(self, ldi):
		self.ldistr = ldi
		self.coefficientlocations = self.getclocation() or []
		self.bound = self.getbound()
	def getbound(self):
		temp = self.ldistr.split('<=')
		return temp[-1]
	def getclocation(self):
		temp = self.ldistr.split('<=')
		cltemps = temp[0].split('+')
		clsequence = []
		for cl in cltemps:
			tempcl = cl.replace('[','').replace(']','').split(',')
			clsequence += [Coefficientlocation(tempcl[0],tempcl[-1])]
		return clsequence

def parseEldi(Eldi):
	eldi = Eldi.replace(' ','').split('#')
	observation = eldi[0]
	eldf = eldi[-1]
	operation = ';'
	ldis = parseELDF(eldf, operation)
	return observation, ldis

def parseELDF(Eldf,operation):
	ldisstr = Eldf.split(operation)
	ldis = []
	for ldistr in ldisstr:
		ldistr = ldistr.replace('(','').replace(')','')
		ldis += [Ldi(ldistr)]
	return ldis

def main():
	file_object = open('eldi.txt')
	eldi = ''
	try:
		eldi = file_object.readlines()
	finally:
		file_object.close()
	print eldi
	observation, ldis = parseEldi(eldi[0].strip())
	print observation
	for ldi in ldis:
		print ldi.ldistr
		for cl in ldi.coefficientlocations:
			print '(' + cl.coefficient + ',' + cl.location + ')'
	
if __name__ == '__main__':
	main()
