from math import sqrt

def is_symetric(A):
	symetric=True
	for i in range(len(A)):
		for j in range(len(A)):
			if A[i][j]!=A[j][i]:
				symetric=False
				break
	return symetric

def cholesky(A):
	if is_symetric(A)==False:
		raise Exception('La matrice n\'est pas symetrique!')
	B=[[0 for i in range(len(A))] for i in range(len(A))]
	for j in range(len(A)):
		B[j][j]=A[j][j]
		for k in range(j):
			B[j][j]=B[j][j]-B[j][k]*B[j][k]
		if B[j][j]<=0:
			raise Exception('La matrice n\'est pas definie positive!')
		B[j][j]=sqrt(B[j][j])
		for i in range(j+1,len(A)):
			B[i][j]=A[i][j]
			for k in range(j):
				B[i][j]=B[i][j]-B[i][k]*B[j][k]
			B[i][j]=B[i][j]/B[j][j]
	return B

A=[[1,1,1,1],[1,5,5,5],[1,5, 14, 14], [1,5,14,15]]
try:
	B=cholesky(A)
	for u in B:
		print u
except Exception:
	print 'Veuillez saisir une matrice qui est symetriquedefinie positive'


			
		
