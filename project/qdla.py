from path import *
from durationinequality import *
from chopinequality import *

"""def buildexist(chopnum, chopineqsstr):
	tau = ''
	for i in range(1, chopnum+1):
		tau = tau + ('m_'+str(i)) + ','
	tau = '{' + tau[:-1] + '}'
	return 'ex(' + tau + ', ' + '('+ chopineqsstr + ')'+')'
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
	print isinstance(eldifile, str)
	templates = parseXML(ntaxml)
	v = Context(['x', 'y', 't'], 'v')
	ceil={v.x:10,v.y:20, v.t:100}
	bgf = v.getZeroFederation()
	beginzone =  Zone('id2', bgf)
	zones,enter = getzones(v,beginzone,templates[0],ceil)
	#ointerval = Observationinterval(15,17,v)
	#spath = Symbolicpath(allpaths[0][0].initzone, allpaths[0][0].path)
	#eldi = '[10,20] # ( [2, id0] + [-3, id1] <= 10) ; ([-4, id1] + [6, id0] <= -7); ([2, id2] <= 0)'
	#observation, ldis = parseEldi(eldi.strip())
	observation, ldis = parseELDI(eldifile)
	observation = observation.replace('[','').replace(']','').replace(' ','')
	lowandup = observation.split(',')
	ointerval = Observationinterval(int(lowandup[0]),int(lowandup[-1]),v)
	
	allpaths = findallpath(enter,ointerval,templates[0])
	chopnum = 2
	i = 0
	qdlas = []
	for pps in allpaths:
		for sp in pps:
			i = i + 1
			spath = Symbolicpath(sp.initzone, sp.path)
			chopineqsstr = chopcondition(spath, chopnum, ldis)
			exist = buildexist(chopnum, chopineqsstr)
			durationineqsstr = potentialpathineqs(v, ointerval, spath, templates[0].transitions)
			qdla = buildforall(v, len(allpaths[0][0].path), durationineqsstr, exist)
			qdlas +=[str(i) + ': '+qdla]
			print str(i) + ': '+qdla
	f = open('qdlaresult.txt','w+')
	f.truncate()
	for qdla in qdlas:
		f.write(qdla)
	f.close()
	end = time.clock()
	print end-start
	return True

if __name__=='__main__':
	main()
