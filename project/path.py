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






def main():
	ointerval = Observationinterval(3,3)
	print ointerval.getOInterval()

if __name__=='__main__':
	main()
