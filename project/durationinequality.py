from path import *
import re
import copy

def initineqs(spath):
	tempfed = spath.initzone.federation
	initzonestr = str(tempfed).replace('(','').replace(')','').replace(' ','').replace('v.','')
	initstr = initzonestr.replace('&', ' and ').replace('==','=')
	return initstr

def findtrans(transitions, path):
	length = len(path)
	trans = []
	if length == 1:
		return trans
	for source, target in zip(range(0, length-1), range(1, length)):
		for tran in transitions:
			if path[source].location == tran.source and path[target].location == tran.target:
				trans +=[tran]
	return trans

def locationfedtoineqs(fed, paralist):
	fedstr = str(fed).replace('(','').replace(')','').replace(' ','')
	#print fedstr
	for para in paralist.keys():
		strinfo = re.compile(para)
		fedstr = strinfo.sub('('+paralist[para]+')', fedstr)
	return fedstr.replace('&', ' and ').replace('==','=')

def buildparalist(context, tran, index, paralist):
	newparalist = copy.deepcopy(paralist)
	assignment = tran.assignment.replace(' ','')
	assignments = assignment.split(',')
	if index == 1:
		assignments +=['t=0']
	assignmentclock = []
	for a in assignments:
		if '=' in a:
			refineda = a.split('=')
			assignmentclock.append(refineda[0])
			value = int(refineda[-1])
			for clock in context.clocks:
				if clock.name in refineda:
					if(value == 0):
						newparalist[context.name+'.'+clock.name] = 't_'+str(index+1)
					else:
						newparalist[context.name+'.'+clock.name] = str(value) + '+' + 't_'+str(index+1)
	for clock in context.clocks:
		if clock.name not in assignmentclock:
			newparalist[context.name+'.'+clock.name] = newparalist[context.name+'.'+clock.name] + '+' + 't_'+str(index+1)
	return newparalist

def firstlocationineqs(fed, context):
	paralist = {}
	for clock in context.clocks:
		paralist[context.name+'.'+clock.name] = clock.name + '+' + 't_0'
	ineqs = locationfedtoineqs(fed, paralist)
	ineqs = ineqs + ' and ' + '0<=t_1<=t_0'
	return ineqs, paralist

def durationineqs(context, spath, transitions):
	ineqs = []
	dineqs = ''
	ineqs += [initineqs(spath)]
	trans = findtrans(transitions, spath.path)
	if len(trans) == 0:
		temp, _ = firstlocationineqs(spath.path[0].federation, context)
		return temp
	firstineqs, paralist = firstlocationineqs(spath.path[0].federation, context)
	ineqs += [firstineqs]
	newparalist = copy.deepcopy(paralist)
	for i in range(1, len(spath.path)):
		newparalist = copy.deepcopy(buildparalist(context, trans[i-1], i, newparalist))
		#print newparalist
		ineqs += [locationfedtoineqs(spath.path[i].federation, newparalist)]
	for i, ineq in zip(range(0, len(ineqs)), ineqs):
		if i == len(ineqs) - 1:
			dineqs = dineqs + ineq
			return dineqs
		dineqs = dineqs + ineq + ' and '

def inboundineq(spath, observation):
	length = len(spath.path)
	temp = ''
	for i in range(1, length+1):
		if i == length:
			temp = temp + 't_' + str(i)
		else:
			temp = temp + 't_' + str(i) + ' + '
	temp = '(' + str(observation.lb)+'<='+temp +'<='+str(observation.ub)+ ')'
	return temp

def nonnegative(spath, context):
	length = len(spath.path)
	nonnega = []
	ineq = ''
	clocknum = len(context.clocks)
	for i in range(0, clocknum):
		temp = '('+ context.clocks[i].name + '>=0'+')'
		nonnega += [temp]
	for i in range(0, length+1):
		temp = '('+'t_' + str(i) + '>=0'+')'
		nonnega += [temp]
	for i in range(0, len(nonnega)):
		if i == len(nonnega)-1:
			ineq = ineq + nonnega[i]
		else:
			ineq = ineq + nonnega[i] + ' and '
	return ineq

def potentialpathineqs(context, observation, spath, transitions):
	dineqs = durationineqs(context, spath, transitions)
	bineq = inboundineq(spath, observation)
	nineqs = nonnegative(spath, context)
	return '(' + dineqs + ' and ' + bineq + ' and ' + nineqs + ')'

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
	"""for pps in allpaths:
		for sp in pps:
			#print isinstance(sp, Symbolicpath)
			pathnum = pathnum + 1
			print sp.initzone.location, sp.initzone.federation
			for sl in sp.path:
				print sl.getsl()
	print pathnum"""
	spath = Symbolicpath(allpaths[0][0].initzone, allpaths[0][0].path)
	print spath.initzone.location, spath.initzone.federation
	for sl in spath.path:
		print sl.getsl()
	#print initineqs(spath)
	trans = findtrans(templates[0].transitions, spath.path)
	for tran in trans:
		print tran.gettransition()
	"""fed = spath.path[0].federation
	firstineqs, paralist = firstlocationineqs(fed, v)
	print firstineqs
	newparalist = buildparalist(v, trans[0], 1, paralist)
	print newparalist
	print locationfedtoineqs(spath.path[1].federation, newparalist)"""
	print potentialpathineqs(v, ointerval, spath, templates[0].transitions)

if __name__ == '__main__':
	main()
