from zonegraph import *
from floyds import *

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

class Symboliclocation:
	def __init__(self, index, locationid, federation):
		self.index = index
		self.location = locationid
		self.federation = federation
		self.valuesymbol = self.getsymbol()
	def getsymbol(self):
		return 't_'+ str(self.index)
	def getfedstr(self):
		return str(self.federation)
	def getsl(self):
		return [self.index, self.location, self.valuesymbol, str(self.federation)]

class Symbolicpath:
	def __init__(self, initzone, sequence):
		self.initzone = initzone
		self.path = sequence[:]

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
	
def forward(ppath, plocation, transitions, context):
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
				if not targetfed.isEmpty() :
					targetzone = Zone(targetlocation, targetfed)
				else:
					targetzone = forward(ppath, plocation, transitions, context)
	else:
		targetzone = backward(ppath, transitions, context)
	return targetzone

def backward(ppath, transitions, context):
	if len(ppath.path)==1:
		return None

	del ppath.path[-1]

	if len(ppath.path)==0:
		return None
	else:
		return forward(ppath, ppath.path[-1], transitions, context)
	
def copypathsequence(ppath):
	sequence = []
	#sequence.append(ppath.initzone)
	for pl in ppath.path:
		sl = Symboliclocation(pl.index, pl.id, pl.federation)
		sequence.append(sl)
	sp = Symbolicpath(ppath.initzone, sequence)
	#return sequence
	return sp

def stayinlocation(plocation, context):
	tempfed = plocation.federation
	if plocation.invariant == None:
		tempfed = plocation.federation.up()
	else :
		tempfed = plocation.federation.up() & invarianttofed(context, plocation.invariant)
	return tempfed

def findallpath(enter, ointerval, template):
	allpaths = []
	for z in enter:
		paths = []
		ppath = Potentialpath(z)
		nextzone, newointerval = dealwithfirstlocation(ppath, ppath.initzone, ointerval, template, paths)
		if len(nextzone)==0:
			findpath(ppath, None, newointerval,template, paths)
		else:
			for zone in nextzone:
				findpath(ppath, zone, newointerval,template, paths)
		#findpath(ppath, ppath.initzone, ointerval,template, paths)
		allpaths += [paths]
	return allpaths

def dealwithfirstlocation(ppath, initzone, ointerval, template, paths):
	location = findlocationbyid(initzone.location, template.locations)
	plocation = PLocation(location, len(ppath.path), initzone.federation)
	plocation.federation = stayinlocation(plocation, ointerval.context)
	plocation.index = plocation.index + 1
	ppath.addPlocation(plocation)
	dbm = fedstrtodbm(str(plocation.federation), ointerval.context)
	floyds(dbm)
	tup = dbm[len(ointerval.context.clocks)][0].value
	newtlow = ointerval.getlb()
	if newtlow - tup <= 0:
		newtlow = 0
		paths.append(copypathsequence(ppath))
	else:
		newtlow = newtlow - tup
	print newtlow
	newointerval = Observationinterval(newtlow,ointerval.getub(),ointerval.context)
	nextzone = []
	while plocation.hasnexttran():
		tranid = plocation.hasnexttran()
		plocation.selecttran(tranid)
		for tran in template.transitions:
			if tran.id == tranid:
				targetlocation = tran.target
				targetfed = None
				if tran.guard != None:
					targetfed = plocation.federation & guardtofed(ointerval.context, tran.guard)
				else:
					targetfed = plocation.federation 
				if tran.assignment != None:
					targetfed = assignmenttofed(ointerval.context, tran.assignment, targetfed)
					targetfed = assignmenttofed(ointerval.context, 't=0', targetfed)
				if not targetfed.isEmpty() :
					targetzone = Zone(targetlocation, targetfed)
					nextzone.append(targetzone)
	return nextzone, newointerval
	
	
def findpath(ppath, zone, ointerval, template, paths):
	initzone = zone
	if initzone is None :
		return

	location = findlocationbyid(initzone.location, template.locations)
	plocation = PLocation(location, len(ppath.path), initzone.federation)

	tempfed = stayinlocation(plocation, ointerval.context)
	isininterval = ininterval(tempfed, ointerval.getOInterval())
	islesslb = lessthanlb(tempfed,ointerval.getlow())
	isgreaterub = greaterthanub(tempfed,ointerval.getup())

	if isininterval:
		plocation.federation = stayinlocation(plocation, ointerval.context)
		plocation.index = plocation.index + 1
		ppath.addPlocation(plocation)
		paths.append(copypathsequence(ppath))
		newzone = forward(ppath, plocation, template.transitions, ointerval.context)
		findpath(ppath, newzone, ointerval, template, paths)
		#return
	elif islesslb:
		plocation.federation = stayinlocation(plocation, ointerval.context)
		plocation.index = plocation.index + 1
		ppath.addPlocation(plocation)
		newzone = forward(ppath, plocation, template.transitions, ointerval.context)
		findpath(ppath, newzone, ointerval, template, paths)
		#return
	elif isgreaterub:
		plocation.federation = stayinlocation(plocation, ointerval.context)
		plocation.index = plocation.index + 1
		ppath.addPlocation(plocation)
		newzone = backward(ppath, template.transitions, ointerval.context)
		findpath(ppath, newzone, ointerval, template, paths)
		#return
	return

def main():
	start = time.clock()
	ntaxml = init(sys.argv[1])
	templates = parseXML(ntaxml)
	v = Context(['x', 'y', 't'], 'v')
	ceil={v.x:10,v.y:20, v.t:100}
	bgf = v.getZeroFederation()
	beginzone =  Zone('id2', bgf)
	zones,enter = getzones(v,beginzone,templates[0],ceil)
	ointerval = Observationinterval(15,17,v)
	allpaths = findallpath(enter,ointerval,templates[0])
	end = time.clock()
	print end-start
	pathnum = 0
	for pps in allpaths:
		for sp in pps:
			#print isinstance(sp, Symbolicpath)
			pathnum = pathnum + 1
			print sp.initzone.location, sp.initzone.federation
			for sl in sp.path:
				print sl.getsl()
	print pathnum

if __name__=='__main__':
	main()
