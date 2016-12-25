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
	for ineqs in conditionineqs:
		if ineqs != conditionineqs[-1]:
			ineqsstr = ineqsstr + ineqs + ' or '
		else:
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
				for slocation in fragments[0]:
					if slocation.location == symbolcl.location:
						if slocation.index != chopcond[i]:
							symbolcl.adddvalue(slocation.getsymbol())
						else:
							symbolcl.adddvalue('m_'+str(i+1))
			ldfineqs.append(ldftoineq(symbolcls))
		if i > 0 and i < len(fragments)-1:
			symbolcls = []
			for cl in ldi.coefficientlocations:
				tempcl = Coefficientlocation(cl.coefficient, cl.location)
				symbolcls.append(tempcl)
			if chopcond[i] == chopcond[i-1]:
				for symbolcl in symbolcls:
					for slocation in fragments[0]:
						if slocation.location == symbolcl.location:
							symbolcl.adddvalue('m_'+str(i+1)+'-'+'m_'+str(i))
				ldfineqs.append(ldftoineq(symbolcls))
			else:
				
def ldftoineq(symbolcls):
	temp=''
	for i, symbolcl in zip(range(0,len(symbolcls)), symbolcls):
		if symbolcl.getcodvalue() != None:
			if i != len(symbolcls)-1:
				temp = temp + symbolcl.getcodvalue() + '+'
			else:
				temp = temp + symbolcl.getcodvalue()
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
		temp = '0<='+'m_'+str(i)+'<='+'t'+str(chop)
		td.append(temp)
	for ineqs in td:
		if ineqs != td[-1]:
			tdineqs = tdineqs + ineqs + ' and '
		else:
			tdineqs = tdineqs + ineqs
	return tdineqs
	
def ADDinequations(chopcond):
	add = []
	addineqs = ''
	for i in range(1, len(chopcond)):
		if chopcond[i] == chopcond[i-1]:
			temp = '('+'m_'+str(i-1)+'<='+'m_'+str(i)+')'
			add.appedn(temp)
	for ineqs in add:
		if ineqs != add[-1]:
			addineqs = addineqs + ineqs + ' and '
		else:
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
