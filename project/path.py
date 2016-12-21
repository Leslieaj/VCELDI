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
	#print plocation.hasnexttran()
	targetzone = None
	if plocation.hasnexttran():
		tranid = plocation.hasnexttran()
		plocation.selecttran(tranid)
		for tran in transitions:
			if tran.id == tranid:
				targetlocation = tran.target
				#print targetlocation
				targetfed = None
				if tran.guard != None:
					targetfed = plocation.federation & guardtofed(context, tran.guard)
				else:
					targetfed = plocation.federation 
				if tran.assignment != None:
					targetfed = assignmenttofed(context, tran.assignment, targetfed)
				if not targetfed.isEmpty() :
					targetzone = Zone(targetlocation, targetfed)
					#print targetzone.location, targetzone.federation
				else:
					targetzone = forward(plocation, transitions, context)

	return targetzone

def backward(ppath, transitions, context):
	if len(ppath.path)==0:
		return None
	newzone = forward(ppath.path[-1], transitions, context)
	if newzone is None:
		del ppath.path[-1]
		return backward(ppath,transitions, context)
	return newzone
	
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

def findallpath(enter, ointerval, template):
	allpaths = []
	for z in enter:
		paths = []
		ppath = Potentialpath(z)
		findpath(ppath, ppath.initzone, ointerval,template, paths)
		allpaths += [paths]
	return allpaths

def findpath(ppath, zone, ointerval, template, paths):
	initzone = zone
	#ppath = Potentialpath(zone)
	if initzone is None :
		return
	location = findlocationbyid(initzone.location, template.locations)
	plocation = PLocation(location, len(ppath.path), initzone.federation)
	#plocation.getplocation()
	tempfed = stayinlocation(plocation, ointerval.context)
	#print tempfed
	isininterval = ininterval(tempfed, ointerval.getOInterval())
	islesslb = lessthanlb(tempfed,ointerval.getlow())
	isgreaterub = greaterthanub(tempfed,ointerval.getup())
	#if len(ppath.path)==0:
		#return
	if isininterval:
		plocation.federation = stayinlocation(plocation, ointerval.context)
		#print plocation.federation
		plocation.index = plocation.index + 1
		ppath.addPlocation(plocation)
		paths.append(copypathsequence(ppath))
		#print plocation.federation
		newzone = forward(plocation, template.transitions, ointerval.context)
		#print newzone.federation
		findpath(ppath, newzone, ointerval, template, paths)
		return
	elif islesslb:
		plocation.federation = plocation.federation.up()
		plocation.index = plocation.index + 1
		newzone = forward(plocation, template.transitions, ointerval.context)
		findpath(ppath, newzone, ointerval, template, paths)
		return
	elif isgreaterub:
		newzone = backward(ppath, template.transitions, ointerval.context)
		if newzone is None:
			return
		findpath(ppath, newzone, ointerval, template, paths)
		return
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
	ointerval = Observationinterval(10,10,v)
	allpaths = findallpath(enter,ointerval,templates[0])
	end = time.clock()
	print end-start
	pathnum = 0
	for pps in allpaths:
		for ps in pps:
			pathnum = pathnum + 1
			for p in range(0, len(ps)):
				if p == 0:
					print ps[0].location, ps[0].federation
				else:
					print ps[p].items()
	print pathnum
	
if __name__=='__main__':
	main()
