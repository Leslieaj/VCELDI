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
	eldfj2 = eldfchop[0].split('and')
	eldfj3j4 = eldfchop[-1].split(')')
	for ldi in eldfj2:
		ldis += [Ldi(ldi.replace('(','').replace(')',''))]
	for ldi in eldfj3j4:
		if ldi != '':
			temp = ldi.replace('and','').replace('or','').replace('(','').replace(')','')
			ldis += [Ldi(temp)]
	"""
	for ldi in ldis:
		print ldi.ldistr, ldi.bound
		for cl in ldi.coefficientlocations:
			print '(' + cl.coefficient + ',' + cl.location + ')'
	"""
	return observation, ldis

def e7Ldfinequations(chopcond, path, ldis):
	fragments = splitpath(chopcond, path)
	ldfineqs = []
	#ldfsJ2 = ldis[:2]
	#ldfsJ3J4 = ldis[2:]
	for i, ldi in zip(range(0,len(ldis)), ldis):
		symbolcls = []
		for cl in ldi.coefficientlocations:
			tempcl = Coefficientlocation(cl.coefficient, cl.location)
			symbolcls.append(tempcl)
		for symbolcl in symbolcls:
			#print 0 if i < 2 else -1
			for slocation in fragments[0 if i < 2 else -1]:
				if slocation.location == symbolcl.location:
					if slocation.index == chopcond[0]:
						if i < 2 :
							symbolcl.adddvalue('m_'+str(1))
						else :
							symbolcl.adddvalue(slocation.getsymbol()+'-'+'m_'+str(1))
					else:
						symbolcl.adddvalue(slocation.getsymbol())
		ldfineqs.append(ldftoineq(symbolcls, ldi.bound))
	lastldf = ldfineqs[-1].replace('<=','<')
	ldfineqs.pop()
	ldfineqs.append(lastldf)
	#print ldfineqs
	ldfsJ2 = ldfineqs[0:2]
	ldfsJ3J4 = ldfineqs[2:]
	return ldfsJ2toineq(ldfsJ2) + 'and' + ldfsJ3J4toineq(ldfsJ3J4)

def ldfsJ2toineq(ldfsJ2):
	return '((' + ldfsJ2[0] + ')' + 'and' + '(' + ldfsJ2[1] + '))'

def ldfsJ3J4toineq(ldfsJ3J4):
	return '((((' + ldfsJ3J4[0] + ') and (' + ldfsJ3J4[1] + ')) or ((' + ldfsJ3J4[2] + ') and (' + ldfsJ3J4[3] + ')))'\
			+ 'and' + '(((' + ldfsJ3J4[4] + ') and (' + ldfsJ3J4[5] + ')) or ((' + ldfsJ3J4[6] + ') and (' + ldfsJ3J4[7] + ')))'\
			+ 'and' + '(' + ldfsJ3J4[8] + '))'

def e7chopcondition(spath, chopnum, ldis):
	pathlen = len(spath.path)
	cctemp = []
	chopconditions = []
	conditionineqs = []
	ineqsstr = ''
	locatechops(chopnum,pathlen,cctemp,chopconditions)
	for chopcond in chopconditions:
		#print chopcond
		LDFsineqs = e7Ldfinequations(chopcond, spath.path, ldis)
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
	v = Context(['x', 'y', 't'], 'v')
	ceil = {v.x:6, v.y:18, v.t:100}
	bgf = v.getZeroFederation()
	beginzone =  Zone('id6', bgf)
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
			chopineqsstr = e7chopcondition(spath, chopnum, ldis)
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
