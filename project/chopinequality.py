from parseeldi import *
from path import Symbolicpath, Symboliclocation

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
		LDFsineqs = Ldfinequations(chopcond, spath.path, ldis)
		TDineqs = TDinequations(chopcond)
		ADDineqs = ADDinequations(chopcond)
		conditionineqs.append('('+LDFsineqs+' and '+TDineqs+' and '+ADDineqs+')')
	for i, ineqs in zip(range(0, len(conditionineqs)), conditionineqs):
		if i != len(conditionineqs)-1:
			ineqsstr = ineqsstr + ineqs + ' or '
		ineqsstr = ineqsstr + ineqs
	return ineqsstr

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
		if i != len(ldfineqs)-1:
			temp = temp + ldefineq + ' and '
		temp = temp + ldefineq
	return temp

def ldftoineq(symbolcls, mbound):
	temp=''
	for i, symbolcl in zip(range(0,len(symbolcls)), symbolcls):
		if symbolcl.getcodvalue() != None:
			if i != len(symbolcls)-1:
				temp = temp + symbolcl.getcodvalue() + '+'
			temp = temp + symbolcl.getcodvalue()
	if temp !='':
		temp = temp + '<=' + mbound
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
		temp = '0<='+'m_'+str(i+1)+'<='+'t'+str(chop)
		td.append(temp)
	for i, ineqs in zip(range(0, len(td)), td):
		if i != len(td)-1:
			tdineqs = tdineqs + ineqs + ' and '
		tdineqs = tdineqs + ineqs
	return tdineqs
	
def ADDinequations(chopcond):
	add = []
	addineqs = ''
	for i in range(1, len(chopcond)):
		if chopcond[i] == chopcond[i-1]:
			temp = '('+'m_'+str(i-1)+'<='+'m_'+str(i)+')'
			add.appedn(temp)
	for i, ineqs in zip(range(0, len(add)), add):
		if i != len(add)-1:
			addineqs = addineqs + ineqs + ' and '
		addineqs = addineqs + ineqs
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

	chopnum = 3
	pathlen = 4
	chopindex = []
	#locatechops(chopnum,pathlen,chopindex)
	#print k
	print buildexist(chopnum, '(kkkk) or (bbbb)')

if __name__=='__main__':
	main()
