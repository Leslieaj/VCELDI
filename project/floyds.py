from python_dbm import Context, Clock

MAX = 10000

def floyds(matrix):
	global MAX
	n = len(matrix)
	for k in range(0, n):
		for i in range(0, n):
			for j in range(0, n):
				if matrix[i][k] != MAX and matrix[k][j]  != MAX and matrix[i][j] > matrix[i][k]+matrix[k][j]:
					matrix[i][j] = matrix[i][k] + matrix[k][j]

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

def lqinineq(ineq, clockindex, dbm):
	temp = ineq.split('<=')
	if is_num_by_except(temp[0]) and (not is_num_by_except(temp[-1])):
		intvalue = int(temp[0])
		if '-' in temp[-1]:
			frag = temp[-1].split('-')
			if (frag[0] in clockindex.keys()) and (frag[-1] in clockindex.keys()):
				index1 = clockindex[frag[-1]]
				index2 = clockindex[frag[0]]
				dbm[index1][index2] = -intvalue
		else:
			if temp[-1] in clockindex.keys():
				index = clockindex[temp[-1]]
				dbm[0][index] = -intvalue
	elif is_num_by_except(temp[-1]) and (not is_num_by_except(temp[0])):
		intvalue = int(temp[-1])
		if '-' in temp[0]:
			frag = temp[0].split('-')
			if (frag[0] in clockindex.keys()) and (frag[-1] in clockindex.keys()):
				index1 = clockindex[frag[0]]
				index2 = clockindex[frag[-1]]
				dbm[index1][index2] = intvalue
		else:
			if temp[0] in clockindex.keys():
				index = clockindex[temp[0]]
				dbm[index][0] = intvalue
	elif (not is_num_by_except(temp[0])) and (not is_num_by_except(temp[-1])):
		frag = temp[:]
		if (frag[0] in clockindex.keys()) and (frag[-1] in clockindex.keys()):
			index1 = clockindex[frag[0]]
			index2 = clockindex[frag[-1]]
			dbm[index1][index2] = 0
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
			lqinineq(temp[-1]+'<='+temp[0], clockindex, dbm)
			lqinineq(newtemp+'<='+newvalue, clockindex, dbm)
		else:
			newvalue = str(-int(temp[0]))
			lqinineq(temp[-1]+'-0'+'<='+temp[0], clockindex, dbm)
			lqinineq('0-'+temp[-1]+'<='+newvalue, clockindex, dbm)
	elif is_num_by_except(temp[-1]) and (not is_num_by_except(temp[0])):
		if '-' in temp[0]:
			frag = temp[0].split('-')
			newtemp = frag[-1]+'-'+frag[0]
			newvalue = str(-int(temp[-1]))
			lqinineq(temp[0]+'<='+temp[-1], clockindex, dbm)
			lqinineq(newtemp+'<='+newvalue, clockindex, dbm)
		else:
			newvalue = str(-int(temp[-1]))
			lqinineq(temp[0]+'-0'+'<='+temp[-1], clockindex, dbm)
			lqinineq('0-'+temp[0]+'<='+newvalue, clockindex, dbm)
	elif (not is_num_by_except(temp[0])) and (not is_num_by_except(temp[-1])):
		lqinineq(temp[0]+'-'+temp[-1]+'<=0', clockindex, dbm)
		lqinineq(temp[-1]+'-'+temp[0]+'<=0', clockindex, dbm)
	else:
		return False
	return True

def setdbmbyineq(ineq, clockindex, dbm):
	ineq = ineq.replace(' ','')
	if '<=' in ineq:
		lqinineq(ineq, clockindex, dbm)
	elif '==' in ineq:
		eqinineq(ineq, clockindex, dbm)
	else:
		return False
	return True

def initdbm(clockindex):
	global MAX
	num = len(clockindex)
	dbm = [[MAX for col in range(num)] for row in range(num)]
	for i in range(0,num):
		if i != len(dbm[0])-1:
			dbm[0][i] = 0
		for j in range(0,num):
			if i==j:
				dbm[i][j] = 0
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
	print matrix[0][0],matrix[0][1],matrix[0][2],matrix[0][3]
	print matrix[1][0],matrix[1][1],matrix[1][2],matrix[1][3]
	print matrix[2][0],matrix[2][1],matrix[2][2],matrix[2][3]
	print matrix[3][0],matrix[3][1],matrix[3][2],matrix[3][3]

if __name__=='__main__':
	main()
