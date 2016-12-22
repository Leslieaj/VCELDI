from parseeldi import *
from path import Symbolicpath, Symboliclocation

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
		conditionineqs.append(LDFsineqs+' and '+TDineqs+' and '+ADDineqs)
	for ineqs in conditionineqs:
		if ineqs != conditionineqs[-1]:
			ineqsstr = ineqsstr + ineqs + ' or '
		else:
			ineqsstr = ineqsstr + ineqs
	return ineqsstr

def Ldfinequations(chopcond, path, ldis):
	fragments = splitpath(chopcond, path)
	for frag, ldi in zip(fragments, ldis):
		
	
def splitpath(chopcond, path):
	fragments = []
	choptemp=1
	for chop in chopcond:
		tempP = path[choptemp-1:chop]
		fragments.append(tempP)
		choptemp = chop
	fragments.append(path[choptemp-1:])
	return fragments


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
	locatechops(chopnum,pathlen,chopindex)

	print k

if __name__=='__main__':
	main()
