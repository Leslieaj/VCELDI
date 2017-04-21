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
	for ldi in eldfj2:
		ldis += ldi.replace('(','').replace(')','')
	print len(eldfj2)
	#ldis += [Ldi(eldfchop[0].replace('(','').replace(')',''))]
	#ldis += [Ldi(eldfchop[-1].replace('(','').replace(')',''))]
	#ldis += [Ldi(eldfand[-1].replace('(','').replace(')',''))]
	#return observation, ldis
"""	
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
	ceil = {v.x:15, v.y:10, v.t:100}
	bgf = v.getZeroFederation()
	beginzone =  Zone('id22', bgf)
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
			chopineqsstr = e6chopcondition(spath, chopnum, ldis)
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
"""
def main():
	#eldifile = sys.argv[2]
	parseexampleELDI('example7.txt')
	
if __name__ == '__main__':
	main()
