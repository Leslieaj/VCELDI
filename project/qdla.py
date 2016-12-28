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

def buildforall(locationnum, durationineqsstr, existpart):
	delta = ''
	for i in range(1, locationnum+1):
		delta = delta + ('t_'+ str(i)) + ','
	delta = '{' + delta[:-1] + '}'
	return 'all(' + delta + ',' + '(' + durationineqsstr + ')' + ' impl ' + existpart + ')'

def main():
	return True

if __name__=='__main__':
	main()
