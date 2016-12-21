from zonegraph import *

class Observationinterval:
	def __init__(self, lower_bound, upper_bound, context):
		self.lb = lower_bound
		self.ub = upper_bound
		self.context = context
	def getlb(self):
		return self.lb
	def getub(self):
		return self.ub
	def getlow(self):
		return guardtofed(self.context, 't<'+str(self.lb))
	def getup(self):
		return guardtofed(self.context, 't>'+str(self.ub))
	def getOInterval(self):
		return guardtofed(self.context, 't>=' + str(self.lb) + '&&' + 't<=' + str(self.ub))

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
		for tranid, hasselected in self.next.items():
			if hasselected == False :
				return tranid
		return False
	def selecttran(self,tranid):
		if tranid in self.next.keys():
			self.next[tranid] = True
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

def lessthanlb(fed,lowfed):
	temp = fed & lowfed
	return not temp.isEmpty()

def greaterthanub(fed, upfed):
	temp = fed & upfed
	return not temp.isEmpty()
	
def ininterval(fed, intervalfed):
	temp = fed & intervalfed
	return not temp.isEmpty()
	
def forward(plocation, transitions, context):
	targetzone = None
	if plocation.hasnexttran():
		tranid = plocation.hasnexttran()
		plocation.selecttran(tranid)
		for tran in transitions:
			if tran.id == tranid:
				targetlocation = tran.target
				targetfed = None
				if tran.guard != None:
					targetfed = plocation.federation & guardtofed(context, tran.guard)
				else:
					targetfed = plocation.federation 
				if tran.assignment != None:
					targetfed = assignmenttofed(context, tran.assignment, targetfed)
				targetzone = Zone(targetlocation, targetfed)
	return targetzone

def backward(ppath, transitions, context):
	forward(ppath[-1], transitions, context)
	
def copypathsequence(ppath):
	sequence = []
	sequence.append(ppath.initzone)
	for pl in ppath.path:
		sequence.append({pl.index:pl.id})
	return sequence
	
def stayinlocation(plocation, context):
	tempfed = plocation.federation
	if plocation.invariant == None:
		tempfed = plocation.federation.up()
	else :
		tempfed = plocation.federation.up() & invarianttofed(context, plocation.invariant)
	return tempfed
	
def findpath(zone, ointerval, template):
	#initzone = zone
	paths = []
	ppath = Potentialpath(zone)
	location = findlocationbyid(zone.location, template.locations)
	plocation = PLocation(location, len(ppath.path), zone.federation)
	#plocation.getplocation()
	tempfed = stayinlocation(plocation, ointerval.context)
	isininterval = ininterval(tempfed, ointerval.getOInterval())
	islesslb = lessthanlb(tempfed,ointerval.getlow())
	isgreaterub = greaterthanub(tempfed,ointerval.getup())
	if isininterval:
		plocation.federation = plocation.federation.up()
		plocation.index = plocation.index + 1
		ppath.addPlocation(plocation)
		paths.append(copypathsequence(ppath))
	#ppath.path[0].getplocation()
	newzone = forward(plocation, template.transitions, ointerval.context)
	ppath.path[0].getplocation()
	print newzone.location, newzone.federation
	print paths[0][0].location,paths[0][0].federation, paths[0][1].items()
	
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
	ointerval = Observationinterval(3,3,v)
	#ointerval = ointervalfed(v,observationinterval)
	findpath(enter[0], ointerval,templates[0])
	
if __name__=='__main__':
	main()
