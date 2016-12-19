from python_dbm.udbm import Context, Clock, Constraint, Federation
from refineinfo import *
from parsexml import *
import time

class Zone:
	def __init__(self, location, federation):
		self.location = location
		self.federation = federation
		
	def __eq__(self, zone):
		if self.location==zone.location and self.federation==zone.federation:
			return True
		else:
			return False

def getzones(context, beginzone, template, ceil):
	needtofind = []
	hasfound = []
	begin = beginzone
	for location in template.locations:
		if location.init == True :
			if location.id == begin.location:
				if location.invariant != None:
					begin.federation = begin.federation.up() & invarianttofed(context, location.invariant)
				else:
					begin.federation = begin.federation.up()
			else:
				print 'the location of the init-zone is not init location'
				return hasfound
	needtofind.append(begin)
	while(len(needtofind)!=0):
		sourcezone = needtofind.pop()
		#print sourcezone.location, sourcezone.federation
		if sourcezone not in hasfound:
			hasfound.append(sourcezone)
			for tran in template.transitions:
				if tran.source == sourcezone.location:
					targetfed = None
					if tran.guard != None:
						targetfed = sourcezone.federation & guardtofed(context, tran.guard)
					else:
						targetfed = sourcezone.federation 
					if tran.assignment != None:
						targetfed = assignmenttofed(context, tran.assignment, targetfed)
					targetlocation = tran.target
					for location in template.locations:
						if targetlocation == location.id:
							if location.invariant != None:
								targetfed = targetfed.up() & invarianttofed(context, location.invariant)
								#print targetfed
							else:
								targetfed = targetfed.up()
							targetfed = targetfed.extrapolateMaxBounds(ceil)
							#print targetfed
					targetzone = Zone(targetlocation, targetfed)
					#if targetzone not in hasfound:
					needtofind.append(targetzone)
	return hasfound
			

def main():
	start = time.clock()
	ntaxml = init(sys.argv[1])
	templates = parseXML(ntaxml)
	v = Context(['x', 'y'], 'v')
	ceil={v.x:10,v.y:20}
	bgf = v.getZeroFederation()
	beginzone =  Zone('id2', bgf)
	zones = getzones(v,beginzone,templates[0],ceil)
	end = time.clock()
	print end-start
	for i in iter(zones):
		print i.location, i.federation
	
if __name__=='__main__':
	main()
