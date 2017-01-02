from path import *
from durationinequality import *
from parseeldi import Coefficientlocation, Ldi
from chopinequality import locatechops, ADDinequations, TDinequations, splitpath, ldftoineq, ldfstoineqs, buildexist

def parseexampleELDI(eldifile):
	file_object = open(eldifile)
	eldi = []
	try:
		eldi = file_object.readlines()
	finally:
		file_object.close()
	#print eldi
	return parseEldi(eldi[0].strip())

def parseEldi(Eldi):
	ldis = []
	eldi = Eldi.replace(' ','').split('#')
	observation = eldi[0]
	eldf = eldi[-1]
	eldfchop = eldf.split(';')
	eldfand = eldfchop[0].split('and')
	ldis += [Ldi(eldfand[0].replace('(','').replace(')',''))]
	ldis += [Ldi(eldfand[-1].replace('(','').replace(')',''))]
	ldis += [Ldi(eldfchop[-1].replace('(','').replace(')',''))]
	return observation, ldis

def e1Ldfinequations(chopcond, path, ldis):
	fragments = splitpath(chopcond, path)
	ldfineqs = []
	ldiand = ldis[:2]
	ldichop = ldis[-1]
	for ldi in ldiand:
		symbolcls = []
		for cl in ldi.coefficientlocations:
			tempcl = Coefficientlocation(cl.coefficient, cl.location)
			symbolcls.append(tempcl)
		for symbolcl in symbolcls:
			for slocation in fragments[0]:
				if slocation.location == symbolcl.location:
					if slocation.index != chopcond[0]:
						symbolcl.adddvalue(slocation.getsymbol())
					else:
						symbolcl.adddvalue('m_'+str(1))
		ldfineqs.append(ldftoineq(symbolcls, ldi.bound))
	symbolcls = []
	for cl in ldichop.coefficientlocations:
		tempcl = Coefficientlocation(cl.coefficient, cl.location)
		symbolcls.append(tempcl)
		for symbolcl in symbolcls:
			for slocation in fragments[-1]:
				if slocation.location == symbolcl.location:
					if slocation.index == chopcond[0]:
						symbolcl.adddvalue(slocation.getsymbol()+'-'+'m_'+str(1))
					else:
						symbolcl.adddvalue(slocation.getsymbol())
	ldfineqs.append(ldftoineq(symbolcls, ldichop.bound))
	return ldfstoineqs(ldfineqs)

def e1chopcondition(spath, chopnum, ldis):
	pathlen = len(spath.path)
	cctemp = []
	chopconditions = []
	conditionineqs = []
	ineqsstr = ''
	locatechops(chopnum,pathlen,cctemp,chopconditions)
	for chopcond in chopconditions:
		#print chopcond
		LDFsineqs = e1Ldfinequations(chopcond, spath.path, ldis)
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

def buildforall(context, locationnum, durationineqsstr, existpart):
	delta = ''
	clock = ''
	clockname = []
	clocknum = len(context.clocks)
	for i in range(0, clocknum):
		clockname += [context.clocks[i].name]
	for i in range(0, len(clockname)):
		if i == len(clockname) - 1:
			clock = clock + clockname[i]
		else:
			clock = clock + clockname[i] + ','
	for i in range(0, locationnum+1):
		delta = delta + ('t_'+ str(i)) + ','
	delta = '{' + delta + clock + '}'
	return 'all(' + delta + ',' + '(' + durationineqsstr + ')' + ' impl ' + existpart + ');\n'

def main():
	start = time.clock()
	ntaxml = init(sys.argv[1])
	eldifile = sys.argv[2]
	templates = parseXML(ntaxml)
	v = Context(['x', 'y', 'z', 't'], 'v')
	ceil = {v.x:3, v.y:4, v.z:2, v.t:100}
	bgf = v.getZeroFederation()
	beginzone =  Zone('id9', bgf)
	zones,enter = getzones(v,beginzone,templates[0],ceil)
	#observation, ldis = parseexampleELDI('example1.txt')
	observation, ldis = parseexampleELDI(eldifile)
	observation = observation.replace('[','').replace(']','').replace(' ','')
	lowandup = observation.split(',')
	ointerval = Observationinterval(int(lowandup[0]),int(lowandup[-1]),v)
	
	allpaths = findallpath(enter,ointerval,templates[0])
	chopnum = 1
	i = 0
	qdlas = []
	for pps in allpaths:
		for sp in pps:
			i = i + 1
			spath = Symbolicpath(sp.initzone, sp.path)
			chopineqsstr = e1chopcondition(spath, chopnum, ldis)
			exist = buildexist(chopnum, chopineqsstr)
			durationineqsstr = potentialpathineqs(v, ointerval, spath, templates[0].transitions)
			qdla = buildforall(v, len(sp.path), durationineqsstr, exist)
			qdlas +=['phi'+ str(i) + ' := '+qdla]
			print 'phi'+ str(i) + ' := '+qdla
	f = open(eldifile.rstrip('.txt')+'result.txt','w+')
	f.truncate()
	f.write('rlset r$\n')
	for i, qdla in zip(range(1, len(qdlas)+1),qdlas):
		outterminator = 'out t;'
		f.write(outterminator+'\n')
		f.write(qdla)
		outfile = 'out ' + eldifile.rstrip('.txt')+ 'result;'
		f.write(outfile+'\n')
		temp = 'rlqe ' + 'phi' + str(i) + ';'
		f.write(temp+'\n')
	f.write('showtime;')
	f.close()
	end = time.clock()
	print end-start

if __name__ == '__main__':
	main()
