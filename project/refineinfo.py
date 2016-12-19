from python_dbm.udbm import Context, Clock, Constraint, Federation
		
def guardtofed(context, guard):
	guard = guard.replace(' ','')
	guards = guard.split('&&')
	gfed = []
	for g in guards:
		if('<=' in g):
			refinedg = g.split('<=')
			clockvaluebound = int(refinedg[-1])
			for clock in context.clocks:
				if clock.name in refinedg:
					gfed.append(Federation(Constraint(clock,None,clockvaluebound,False)))
		elif('<' in g):
			refinedg = g.split('<')
			clockvaluebound = int(refinedg[-1])
			for clock in context.clocks:
				if clock.name in refinedg:
					gfed.append(Federation(Constraint(clock,None,clockvaluebound,True)))
		elif('>=' in g):
			refinedg = g.split('>=')
			clockvaluebound = int(refinedg[-1])
			for clock in context.clocks:
				if clock.name in refinedg:
					gfed.append(Federation(Constraint(None,clock,0-clockvaluebound,False)))
		elif('>' in g):
			refinedg = g.split('>')
			clockvaluebound = int(refinedg[-1])
			for clock in context.clocks:
				if clock.name in refinedg:
					gfed.append(Federation(Constraint(None,clock,0-clockvaluebound,True)))
		elif('==' in g):
			refinedg = g.split('==')
			clockvaluebound = int(refinedg[-1])
			for clock in context.clocks:
				if clock.name in refinedg:
					gfed.append(Federation(Constraint(clock,None,clockvaluebound,False)))
					gfed.append(Federation(Constraint(None,clock,0-clockvaluebound,False)))
		else:
			print "error in guard to federation"
	fed = gfed[0]
	for f in gfed:
		fed = fed&f
	return fed

def assignmenttofed(context, assignment, fedaration):
	assignment = assignment.replace(' ','')
	assignments = assignment.split(',')
	afed = fedaration
	for a in assignments:
		if('=' in a):
			refineda = a.split('=')
			value = int(refineda[-1])
			for clock in context.clocks:
				if clock.name in refineda:
					if(value == 0):
						afed = afed.resetValue(clock)
					else:
						afed = afed.updateValue(clock,value)
	return afed

def invarianttofed(context, invariant):
	ifed = guardtofed(context, invariant)
	return ifed
"""
def main():

	v1 = Context(['x','y'],'v')
	guard = ' x<= 8 && x >= 8'
	fed=guardtofed(v1,guard)
	print fed
	
	_fed = fed[0]
	for f in fed:
		_fed = _fed&f
	print _fed
	assignment = ' x=0, y= 9 '
	afed = assignmenttofed(v1,assignment,_fed)
	print afed
	
if __name__=='__main__':
	main()
"""
