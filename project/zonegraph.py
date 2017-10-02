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
	enterpoint = []
	begin = beginzone
	enterpoint.append(Zone(begin.location,begin.federation))
	for location in template.locations:
		if location.init == True :
			if location.id == begin.location:
				if location.invariant != None:
					begin.federation = begin.federation.up() & invarianttofed(context, location.invariant)
					begin.federation = assignmenttofed(context, 't=0', begin.federation)
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
					if not targetfed.isEmpty() :
						targetfed = assignmenttofed(context, 't=0', targetfed)
						targetfed = targetfed.extrapolateMaxBounds(ceil)
						enterzone = Zone(targetlocation, targetfed)
						if enterzone not in enterpoint:
							enterpoint.append(enterzone)
					for location in template.locations:
						if targetlocation == location.id:
							if location.invariant != None:
								targetfed = targetfed.up() & invarianttofed(context, location.invariant)
							else:
								targetfed = targetfed.up()
							targetfed = targetfed.extrapolateMaxBounds(ceil)
					if not targetfed.isEmpty() :
						targetfed = assignmenttofed(context, 't=0', targetfed)
						targetzone = Zone(targetlocation, targetfed)
						needtofind.append(targetzone)
	return hasfound, enterpoint

def main():
	start = time.clock()
	ntaxml = init(sys.argv[1])
	templates = parseXML(ntaxml)
	v = Context(['x', 'y', 't'], 'v')
	#v = Context(['x', 'y', 'z', 't'], 'v')
	ceil={v.x:15,v.y:10, v.t:100}
	#ceil = {v.x:3, v.y:4, v.z:2, v.t:100}
	bgf = v.getZeroFederation()
	#print bgf
	beginzone =  Zone('id57', bgf)
	#beginzone =  Zone('id9', bgf)
	zones,enter = getzones(v,beginzone,templates[0],ceil)
	end = time.clock()
	print end-start
	for i in iter(zones):
		if i.location == 'id57':
			print i.location, i.federation
	for j in iter(enter):
		if j.location == 'id57':
			print j.location, j.federation
	print len(enter)
	print len(zones)
if __name__=='__main__':
	main()

