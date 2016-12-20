from zonegraph import *

class Observationinterval:
	def __init__(self, lower_bound, upper_bound):
		self.lb = lower_bound
		self.ub = upper_bound
	def getlb(self):
		return self.lb
	def getub(self):
		return self.ub
	def getOInterval(self):
		return '[' + str(self.lb) + ',' + str(self.ub) + ']'

class PLocation:
	def __init__(self, locationid, index, federation)
		self.id = locationid
		self.index = index
		self.federation = federation
	def getLocationVariable()
		return 't_'+ str(self.index)


class Potentialpath:
	def __init__(self, initzone)
		self.initzone = initzone
		self.path = []
	def addPlocation(self, plocation)
		self.path.append(plocation)
	

def findpath(zone, observationinterval):
	initzone = zone
	paths = []
	
	



def main():
	ointerval = Observationinterval(3,3)
	print ointerval.getOInterval()

if __name__=='__main__':
	main()
