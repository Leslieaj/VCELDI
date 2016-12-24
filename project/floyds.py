from python_dbm import Context, Clock



class Distance:
	def __init__(self, value, symbol):
		self.value = value
		self.symbol = symbol
	def __add__(self, right):
		global MAX
		tempvalue = self.value + right.value
		if  tempvalue >= MAX.value:
			dis = Distance(MAX.value,'<=')
			return dis
		else:
			if self.symbol == '<=' and right.symbol == '<=':
				dis = Distance(tempvalue,'<=')
				return dis
			else:
				dis = Distance(tempvalue,'<')
				return dis
	def __lt__(self, right):
		if self.value < right.value:
			return True
		elif self.value > right.value:
			return False
		else:
			if self.symbol == '<' and right.symbol == '<=':
				return True
			elif self.symbol == '<=' and right.symbol == '<':
				return False
			else:
				return False
	def __eq__(self, right):
		if self.value == right.value and self.symbol == right.symbol:
			return True
		else:
			return False
	def __ne__(self, right):
		return not (self==right)
	def __str__(self):
		return '(' + str(self.value) + ',' + self.symbol + ')'

MAX = Distance(10000, '<=')

def floyds(matrix):
	global MAX
	n = len(matrix)
	for k in range(0, n):
		for i in range(0, n):
			for j in range(0, n):
				if matrix[i][k] != MAX and matrix[k][j]  != MAX and  matrix[i][k]+matrix[k][j] < matrix[i][j]:
					matrix[i][j].value = (matrix[i][k] + matrix[k][j]).value
					matrix[i][j].symbol = (matrix[i][k] + matrix[k][j]).symbol

def is_num_by_except(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

def getclockindex(context):
	clockindex = {}
	for clock in context.clocks:
		clockindex[clock.name]=clock.index+1
	return clockindex

def lqorltinineq(ineq, clockindex, symbol, dbm):
	temp = ineq.split(symbol)
	if is_num_by_except(temp[0]) and (not is_num_by_except(temp[-1])):
		intvalue = int(temp[0])
		if '-' in temp[-1]:
			frag = temp[-1].split('-')
			if (frag[0] in clockindex.keys()) and (frag[-1] in clockindex.keys()):
				index1 = clockindex[frag[-1]]
				index2 = clockindex[frag[0]]
				dbm[index1][index2].value = -intvalue
				dbm[index1][index2].symbol = symbol
		else:
			if temp[-1] in clockindex.keys():
				index = clockindex[temp[-1]]
				dbm[0][index].value = -intvalue
				dbm[0][index].symbol = symbol
	elif is_num_by_except(temp[-1]) and (not is_num_by_except(temp[0])):
		intvalue = int(temp[-1])
		if '-' in temp[0]:
			frag = temp[0].split('-')
			if (frag[0] in clockindex.keys()) and (frag[-1] in clockindex.keys()):
				index1 = clockindex[frag[0]]
				index2 = clockindex[frag[-1]]
				dbm[index1][index2].value = intvalue
				dbm[index1][index2].symbol = symbol
		else:
			if temp[0] in clockindex.keys():
				index = clockindex[temp[0]]
				dbm[index][0].value = intvalue
				dbm[index][0].symbol = symbol
	elif (not is_num_by_except(temp[0])) and (not is_num_by_except(temp[-1])):
		frag = temp[:]
		if (frag[0] in clockindex.keys()) and (frag[-1] in clockindex.keys()):
			index1 = clockindex[frag[0]]
			index2 = clockindex[frag[-1]]
			dbm[index1][index2].value = 0
			dbm[index1][index2].symbol = symbol
	else:
		return False
	return True

def eqinineq(ineq, clockindex, dbm):
	temp = ineq.split('==')
	if is_num_by_except(temp[0]) and (not is_num_by_except(temp[-1])):
		if '-' in temp[-1]:
			frag = temp[-1].split('-')
			newtemp = frag[-1]+'-'+frag[0]
			newvalue = str(-int(temp[0]))
			lqorltinineq(temp[-1]+'<='+temp[0], clockindex, '<=', dbm)
			lqorltinineq(newtemp+'<='+newvalue, clockindex, '<=', dbm)
		else:
			newvalue = str(-int(temp[0]))
			lqorltinineq(temp[-1]+'-0'+'<='+temp[0], clockindex, '<=', dbm)
			lqorltinineq('0-'+temp[-1]+'<='+newvalue, clockindex, '<=', dbm)
	elif is_num_by_except(temp[-1]) and (not is_num_by_except(temp[0])):
		if '-' in temp[0]:
			frag = temp[0].split('-')
			newtemp = frag[-1]+'-'+frag[0]
			newvalue = str(-int(temp[-1]))
			lqorltinineq(temp[0]+'<='+temp[-1], clockindex, '<=', dbm)
			lqorltinineq(newtemp+'<='+newvalue, clockindex, '<=', dbm)
		else:
			newvalue = str(-int(temp[-1]))
			lqorltinineq(temp[0]+'-0'+'<='+temp[-1], clockindex, '<=', dbm)
			lqorltinineq('0-'+temp[0]+'<='+newvalue, clockindex, '<=', dbm)
	elif (not is_num_by_except(temp[0])) and (not is_num_by_except(temp[-1])):
		lqorltinineq(temp[0]+'-'+temp[-1]+'<=0', clockindex, '<=', dbm)
		lqorltinineq(temp[-1]+'-'+temp[0]+'<=0', clockindex, '<=', dbm)
	else:
		return False
	return True

def setdbmbyineq(ineq, clockindex, dbm):
	ineq = ineq.replace(' ','')
	if '<=' in ineq:
		lqorltinineq(ineq, clockindex, '<=', dbm)
	elif '==' in ineq:
		eqinineq(ineq, clockindex, dbm)
	elif '<' in ineq:
		lqorltinineq(ineq, clockindex, '<', dbm)
	else:
		return False
	return True

def initdbm(clockindex):
	global MAX
	num = len(clockindex)
	dbm = [[Distance(10000, '<=') for col in range(num)] for row in range(num)]
	for i in range(0,num):
		if i != len(dbm[0])-1:
			dbm[0][i].value = 0
		for j in range(0,num):
			if i==j:
				dbm[i][j].value = 0
	return dbm
	
def fedstrtodbm(fedstr,context):
	clockindex = getclockindex(context)
	clockindex['0'] = 0
	dbm = initdbm(clockindex)
	temp = fedstr
	temp = temp.replace('(','').replace(')','').replace(' ','').replace('v.','')
	ineqs = temp.split('&')
	for ineq in ineqs:
		setdbmbyineq(ineq, clockindex, dbm)
	return dbm

def main():
	global MAX
	v = Context(['x','y','t'],'v')
	fedstr='(v.x<=10 & v.x==v.t & v.y-v.x<=-5)'
	matrix = fedstrtodbm(fedstr,v)
	for i in matrix:
		for j in i:
			print j
	floyds(matrix)
	print str(matrix[0][0]),str(matrix[0][1]),str(matrix[0][2]),str(matrix[0][3])
	print str(matrix[1][0]),str(matrix[1][1]),str(matrix[1][2]),str(matrix[1][3])
	print str(matrix[2][0]),str(matrix[2][1]),str(matrix[2][2]),str(matrix[2][3])
	print str(matrix[3][0]),str(matrix[3][1]),str(matrix[3][2]),str(matrix[3][3])

if __name__=='__main__':
	main()
