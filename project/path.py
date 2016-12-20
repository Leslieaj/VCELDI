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
		return 't>=' + str(self.lb) + '&&' + 't<=' + str(self.ub) 

class PLocation:
	def __init__(self, location, index, federation):
		self.id = location.id
		self.index = index
		self.invariant = location.invariant
		self.federation = federation
		self.next = self.initnext(location) or {}
	def initnext(self, location):
		nexttr = {}
		#print location.next
		for key, value in location.next.items():
			nexttr[key] = value
		return nexttr
	def getLocationVariable(self):
		return 't_'+ str(self.index)
	#if there is an out transition has not been selected, return the tansition id, 
	#	else, means all out transitions of the location have selected, return False.
	def hasnexttran(self):
		for tranid, hasselected in next:
			if hasselected == False :
				return tranid
		return False
	def selecttran(self,tranid):
		if tranid in next.keys():
			next[tranid] = True
	def getplocation(self):
		print self.id,self.index, self.invariant, self.federation, self.next
		
class Potentialpath:
	def __init__(self, initzone):
		self.initzone = initzone
		self.path = []
	def addPlocation(self, plocation):
		self.path.append(plocation)

def findlocationbyid(id, locations):
	for l in locations:
		if id == l.id:
			#print l.next
			return l
	return None

def ointervalfed(context, ointerval):
	interval = ointerval.getOInterval()
	return guardtofed(context, interval)

def findpath(zone, ointerval, template):
	initzone = zone
	paths = []
	ppath = Potentialpath(initzone)
	location = findlocationbyid(initzone.location, template.locations)
	plocation = PLocation(location, len(ppath.path), initzone.federation)
	#plocation.getplocation()
	if plocation.invariant == None:
		tempfed = plocation.federation.up() & ointerval
		if not tempfed.isEmpty():
			plocation.federation = plocation.federation.up()
			plocation.index = plocation.index + 1
			ppath.addPlocation(plocation)
	ppath.path[0].getplocation()


def main():
	#start = time.clock()
	ntaxml = init(sys.argv[1])
	templates = parseXML(ntaxml)
	v = Context(['x', 'y', 't'], 'v')
	ceil={v.x:10,v.y:20, v.t:100}
	bgf = v.getZeroFederation()
	beginzone =  Zone('id2', bgf)
	zones,enter = getzones(v,beginzone,templates[0],ceil)
	#end = time.clock()
	#print end-start
	observationinterval = Observationinterval(3,3)
	ointerval = ointervalfed(v,observationinterval)
	findpath(enter[0], ointerval,templates[0])
	
if __name__=='__main__':
	main()
