from parseeldi import *
from path import *

def buildexist(chopnum, chopineqsstr):
	tau = ''
	for i in range(1, chopnum+1):
		tau = tau + ('m_'+str(i)) + ','
	tau = '{' + tau[:-1] + '}'
	return 'ex(' + tau + ', ' + '('+ chopineqsstr + ')'+')'

def chopcondition(spath, chopnum, ldis):
	pathlen = len(spath.path)
	cctemp = []
	chopconditions = []
	conditionineqs = []
	ineqsstr = ''
	locatechops(chopnum,pathlen,cctemp,chopconditions)
	for chopcond in chopconditions:
		#print chopcond
		LDFsineqs = Ldfinequations(chopcond, spath.path, ldis)
		TDineqs = TDinequations(chopcond)
		ADDineqs = ADDinequations(chopcond)
		if ADDineqs != None:
			conditionineqs.append('('+LDFsineqs+' and '+TDineqs+' and '+ADDineqs+')')
		else:
			conditionineqs.append('('+LDFsineqs+' and '+TDineqs+')')
	for i, ineqs in zip(range(0, len(conditionineqs)), conditionineqs):
		if i == len(conditionineqs)-1:
			ineqsstr = ineqsstr + ineqs
			return ineqsstr
		ineqsstr = ineqsstr + ineqs + ' or '

def Ldfinequations(chopcond, path, ldis):
	fragments = splitpath(chopcond, path)
	ldfineqs = []
	for i, ldi in zip(range(0,len(fragments)), ldis):
		if i == 0:
			symbolcls = []
			for cl in ldi.coefficientlocations:
				tempcl = Coefficientlocation(cl.coefficient, cl.location)
				symbolcls.append(tempcl)
			for symbolcl in symbolcls:
				for slocation in fragments[i]:
					if slocation.location == symbolcl.location:
						if slocation.index != chopcond[i]:
							symbolcl.adddvalue(slocation.getsymbol())
						else:
							symbolcl.adddvalue('m_'+str(i+1))
			#print symbolcl.dvalue
			ldfineqs.append(ldftoineq(symbolcls, ldi.bound))
		elif i > 0 and i < len(fragments)-1:
			symbolcls = []
			for cl in ldi.coefficientlocations:
				tempcl = Coefficientlocation(cl.coefficient, cl.location)
				symbolcls.append(tempcl)
			if chopcond[i] == chopcond[i-1]:
				for symbolcl in symbolcls:
					for slocation in fragments[i]:
						if slocation.location == symbolcl.location:
							symbolcl.adddvalue('m_'+str(i+1)+'-'+'m_'+str(i))
			else:
				for symbolcl in symbolcls:
					for slocation in fragments[i]:
						if slocation.location == symbolcl.location:
							if slocation.index == chopcond[i-1]:
								symbolcl.adddvalue(slocation.getsymbol()+'-'+'m_'+str(i))
							elif slocation.index == chopcond[i]:
								symbolcl.adddvalue('m_'+str(i+1))
							else:
								symbolcl.adddvalue(slocation.getsymbol())
			ldfineqs.append(ldftoineq(symbolcls, ldi.bound))
		else:
			symbolcls = []
			for cl in ldi.coefficientlocations:
				tempcl = Coefficientlocation(cl.coefficient, cl.location)
				symbolcls.append(tempcl)
			for symbolcl in symbolcls:
				for slocation in fragments[i]:
					if slocation.location == symbolcl.location:
						if slocation.index == chopcond[i-1]:
							symbolcl.adddvalue(slocation.getsymbol()+'-'+'m_'+str(i))
						else:
							symbolcl.adddvalue(slocation.getsymbol())
			ldfineqs.append(ldftoineq(symbolcls, ldi.bound))
	return ldfstoineqs(ldfineqs)

def ldfstoineqs(ldfineqs):
	temp = ''
	for i, ldefineq in zip(range(0,len(ldfineqs)), ldfineqs):
		if i == len(ldfineqs)-1:
			temp = temp + ldefineq
			return temp
		temp = temp + ldefineq + ' and '
	return temp

def ldftoineq(symbolcls, mbound):
	temp=''
	for i, symbolcl in zip(range(0,len(symbolcls)), symbolcls):
		if symbolcl.getcodvalue() != None:
			if i == len(symbolcls)-1:
				temp = temp + symbolcl.getcodvalue()
			else:
				temp = temp + symbolcl.getcodvalue() + '+'
	if temp !='':
		temp = temp + '<=' + mbound
	#else:
		#temp = '0<='+mbound
	return temp

def splitpath(chopcond, path):
	fragments = []
	choptemp=1
	for chop in chopcond:
		tempP = path[choptemp-1:chop]
		fragments.append(tempP)
		choptemp = chop
	fragments.append(path[choptemp-1:])
	return fragments

def TDinequations(chopcond):
	td = []
	tdineqs = ''
	for i, chop in zip(range(0,len(chopcond)), chopcond):
		temp = '('+'0<='+'m_'+str(i+1)+'<='+'t_'+str(chop)+')'
		td.append(temp)
	for i, ineqs in zip(range(0, len(td)), td):
		if i == len(td)-1:
			tdineqs = tdineqs + ineqs
			return tdineqs
		tdineqs = tdineqs + ineqs + ' and '
	return tdineqs
	
def ADDinequations(chopcond):
	add = []
	addineqs = ''
	for i in range(1, len(chopcond)):
		if chopcond[i] == chopcond[i-1]:
			temp = '('+'m_'+str(i-1+1)+'<='+'m_'+str(i+1)+')'
			add.append(temp)
	if len(add) == 0:
		return None
	for i, ineqs in zip(range(0, len(add)), add):
		if i == len(add)-1:
			addineqs = addineqs + ineqs
			return addineqs
		addineqs = addineqs + ineqs + ' and '
	return addineqs
k=0

def locatechops(chopnum, pathlen, ci, chopconditions):
	global k
	m = 1
	if chopnum > 1:
		if len(ci) > 0:
			m = ci[-1]
		for index in range(m, pathlen+1):
			ci.append(index)
			locatechops(chopnum-1, pathlen, ci, chopconditions)
			del ci[-1]
	elif chopnum == 1:
		if len(ci) > 0:
			m = ci[-1]
		for index in range(m, pathlen+1):
			ci.append(index)
			cc = ci[:]
			chopconditions.append(cc)
			k = k+1
			del ci[-1]
	else:
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
	chopnum = 2
	eldi = '[10,20] # ( [2, id0] + [-3, id1] <= 10) ; ([-4, id1] + [6, id0] <= -7); ([2, id2] <= 0)'
	observation, ldis = parseEldi(eldi.strip())
	"""for ldi in ldis:
		print ldi.ldistr
		for cl in ldi.coefficientlocations:
			print '(' + cl.coefficient + ',' + cl.location + ')' """
	chopineqsstr = chopcondition(spath, chopnum, ldis)
	exist = buildexist(chopnum, chopineqsstr)
	print exist

if __name__=='__main__':
	main()
