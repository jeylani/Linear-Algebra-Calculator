import numpy as np

def convert_numpy_matrix(matrix):
	return [[float(x) for x in v] for v in matrix]
	
def diag(vector):
	matrix=[[0 for i in vector] for j in vector]
	for i in range(len(vector)):
		matrix[i][i]=vector[i]
	return matrix
def puissance(matrix,n):
	if n==0:
		return diag([1]*n)
	elif n<0:
		puissance(np.linalg.inv(matrix),n)
	else :
		res=numpy.linalg.eig(calcul['operandes'])
		P=res[1].transpose()
		spectre=[float(v)**n for v in res[0] ]	
		D=diag(spectre)
		X=np.dot(P,D)
	 	X=np.dot(X,np.linalg.inv(P))
	 	return convert_numpy_matrix(X)
