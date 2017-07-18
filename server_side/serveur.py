#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 08:29:44 2017

@author: jeylani
"""
import socket
import json
import threading
import numpy
from scipy import linalg

def menu():
	print("0: Afficher la liste des clients connectes")
        print("1: Arreter le serveur")
        print("Quel est votre requete?")
        
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
		puissance(numpy.linalg.inv(matrix),n)
	else :
		res=numpy.linalg.eig(matrix)
		P=res[1]
		P=convert_numpy_matrix(P)
		print P
		spectre=[float(v)**n for v in res[0] ]	
		D=diag(spectre)
		print D
		X=numpy.dot(P,D)
		invP=numpy.linalg.inv(P)
		print invP
	 	X=numpy.dot(X,invP)
	 	return convert_numpy_matrix(X)
	
class ClientThread(threading.Thread):
        def __init__(self,ip,port,client_socket):
                threading.Thread.__init__(self)
                self.ip=ip
                self.port=port
                self.client_socket=client_socket
                print("[+] Un client utilisant l'adresse %s et le port %s s'est connecte au serveur!" % (self.ip, self.port))
                menu()
        def run(self):
                try:
                        while True:
                                try:
                                        request=self.client_socket.recv(1024)
                                        calcul=json.loads(request)
                                        if calcul['operateur']=='DISCONNECT':
                                                break
                                        elif calcul['operateur']=='+':
                                                a=float(calcul['operandes'][0])
                                                b=float(calcul['operandes'][1])
                                                self.client_socket.send(json.dumps({'result':a+b}))
                                        elif calcul['operateur']=='-':
                                                a=float(calcul['operandes'][0])
                                                b=float(calcul['operandes'][1])
                                                self.client_socket.send(json.dumps({'result':a-b}))
                                        elif calcul['operateur']=='*':
                                                a=float(calcul['operandes'][0])
                                                b=float(calcul['operandes'][1])
                                                self.client_socket.send(json.dumps({'result':a*b}))
                                        elif calcul['operateur']=='/':
                                                a=float(calcul['operandes'][0])
                                                b=float(calcul['operandes'][1])
                                                self.client_socket.send(json.dumps({'result':a/b}))
                                        elif calcul['operateur']=='INV':
                                                res=numpy.linalg.inv(calcul['operandes'])
                                                matrix=[[float(x) for x in v] for v in res]
                                                response=json.dumps({'result':matrix})
                                                #print 'Taille de la reponse %s ' %len(response)
                                                #print response
                                                self.client_socket.send(response)
                                        elif calcul['operateur']=='TRANS':
                                                res=numpy.transpose(calcul['operandes'])
                                                matrix=convert_numpy_matrix(res)
                                                response=json.dumps({'result':matrix})
                                                #print 'Taille de la reponse %s ' %len(response)
                                                #print response
                                                self.client_socket.send(response)
                                        elif calcul['operateur']=='DET':
                                                res=numpy.linalg.det(calcul['operandes'])
                                                response=json.dumps({'result':res})
                                                #print 'Taille de la reponse %s ' %len(response)
                                                #print response
                                                self.client_socket.send(response)
                                        elif calcul['operateur']=='TR':
                                                res=numpy.trace(calcul['operandes'])
                                                response=json.dumps({'result':res})
                                                #print 'Taille de la reponse %s ' %len(response)
                                                #print response
                                                self.client_socket.send(response)
                       			elif calcul['operateur']=='PROD':
                       				A=calcul['operandes'][0]
                       				B=calcul['operandes'][1]
                       				if len(A[0])!=len(B):
                       					err="Les dimensions des deux matrices ne sont pas valides pour faire la multiplication!"
                       					response=json.dumps({'error':err})
                                                else:
                                                	res=numpy.dot(A,B)
                                                	matrix=convert_numpy_matrix(res)
                                                	response=json.dumps({'result':matrix})
                                        	#print 'Taille de la reponse %s '%len(response)
                                        	self.client_socket.send(response)
                                     	elif calcul['operateur']=='SOM':
                       				a=numpy.array(calcul['operandes'][0])
                       				b=numpy.array(calcul['operandes'][1])
                       				if len(a)==len(b) and len(a[0])==len(b[0]):
		                                        res=a+b
		                                        matrix=convert_numpy_matrix(res)
		                                        response=json.dumps({'result':matrix})
	                                        else:
	                                        	err="Les deux matrices doivent avoir les memes dimensions!"
                       					response=json.dumps({'error':err})
                                                #print 'Taille de la reponse %s ' %len(response)
                                                #print response
                                                self.client_socket.send(response)
                                        elif calcul['operateur']=='DIFF':
                       				a=numpy.array(calcul['operandes'][0])
                       				b=numpy.array(calcul['operandes'][1])
                       				if len(a)==len(b) and len(a[0])==len(b[0]):
		                                        res=a-b
		                                        matrix=convert_numpy_matrix(res)
		                                        response=json.dumps({'result':matrix})
	                                        else:
	                                        	err="Les deux matrices doivent avoir les memes dimensions!"
                       					response=json.dumps({'error':err})
                                                #print 'Taille de la reponse %s ' %len(response)
                                                #print response
                                                self.client_socket.send(response)
                                        elif calcul['operateur']=='SL':
                       				a=numpy.array(calcul['operandes'][0])
                       				y=numpy.array(calcul['operandes'][1])
                                                res=numpy.linalg.solve(a, y)
                                                vector=[ [float(v)] for v in res]
                                                response=json.dumps({'result':vector})
                                                #print 'Taille de la reponse %s ' %len(response)
                                                #print response
                                                self.client_socket.send(response)
                                        elif calcul['operateur']=='SPEC':
                       				res=numpy.linalg.eig(calcul['operandes'])
                                                vector=[[ float(v) for v in res[0] ]]
                                                response=json.dumps({'result':vector})
                                                #print 'Taille de la reponse %s ' %len(response)
                                                #print response
                                                self.client_socket.send(response)
                       			elif calcul['operateur']=='VP':
                       				res=numpy.linalg.eig(calcul['operandes'])
                       				w=res[1].transpose()
                                                matrix=convert_numpy_matrix(w)
                                                response=json.dumps({'result':matrix})
                                                #print 'Taille de la reponse %s ' %len(response)
                                                #print response
                                                self.client_socket.send(response)
                                        elif calcul['operateur']=='CHOLESKY':
                       				res=numpy.linalg.cholesky(calcul['operandes'])
                                                matrix=convert_numpy_matrix(res)
                                                response=json.dumps({'result':matrix})
                                                #print 'Taille de la reponse %s ' %len(response)
                                                #print response
                                                self.client_socket.send(response)
                                        elif calcul['operateur']=='CHOLESKY':
                       				res=numpy.linalg.cholesky(calcul['operandes'])
                                                matrix=convert_numpy_matrix(res)
                                                response=json.dumps({'result':matrix})
                                                #print 'Taille de la reponse %s ' %len(response)
                                                #print response
                                                self.client_socket.send(response)
                                        elif calcul['operateur']=='LU':
                       				L,U=linalg.lu(calcul['operandes'],permute_l=True)
                                                matrix=convert_numpy_matrix(L)
                                                matrix2=convert_numpy_matrix(U)
                                                response=json.dumps({'result':matrix,'result2':matrix2})
                                                #print 'Taille de la reponse %s ' %len(response)
                                                #print response
                                                self.client_socket.send(response)
                                        elif calcul['operateur']=='PUIS':
                                                matrix=puissance(calcul['operandes'][0], calcul['operandes'][1])
                                                response=json.dumps({'result':matrix})
                                                #print 'Taille de la reponse %s ' %len(response)
                                                #print response
                                                self.client_socket.send(response)
                                        else:
                                       		self.client_socket.send(json.dumps({'error':"Cet operateur n'est pas encore pris en charge!"}))
                      		
                      		except numpy.linalg.linalg.LinAlgError as err:
                                	if err.message=='Singular matrix':
                                        	self.client_socket.send(json.dumps({'error':"La matrice saisie n'est pas inversible!"}))
                                	elif err.message=='Matrix is not positive definite':
                                		self.client_socket.send(json.dumps({'error':"La matrice saisie n'est pas definie positive!"}))
                                	else:
                                		self.client_socket.send(json.dumps({'error':err.message}))
                                except (NameError,TypeError) as err:
                                	mess="Les valeurs saisies sont incompletes!: "+err.message
                                        self.client_socket.send(json.dumps({'error':mess}))				
                                except ZeroDivisionError :
                                        self.client_socket.send(json.dumps({'error':"Imposible de diviser un nombre par zero"}))	
                                except ValueError as err:
                                        self.client_socket.send(json.dumps({'error':"L'une des valeurs saisie est invalide!: "+err.message}))
                                

                except socket.error as msg:
                        print 'Erreur socket:%s'%msg
                        menu()	
                finally:
                        self.client_socket.close()
class ServerThread(threading.Thread):
        def __init__(self,sock,port=15555):
                threading.Thread.__init__(self)
                self.sock=sock
                self.arret=False
                self.port=port
                self.clients=list()
        def run(self):
                threads=list()
                
                while not self.arret:
                        self.sock.listen(5)
                        (client_socket, (ip,port)) = self.sock.accept()
                        if not self.arret: 
                        	client_thread=ClientThread(ip, port, client_socket)
                        	threads.append(client_thread)
                        	self.clients.append((ip,port))
                        	client_thread.start()
                for thread in threads:
                        thread.join()
        def shutdown(self):
        	print "Veuillez deconnecter tous les clients qui communiquent avec moi!"
        	print "Fermeture du serveur en cours..."
                self.arret=True
                temp_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		temp_sock.connect(('127.0.0.1',self.port))
		temp_sock.send('{"operateur":"DISCONNECT"}')
		temp_sock.close()

	
try:	
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Demmarage du Serveur'
        port=input('Veuillez saisir un numero de port pour le serveur:')
        sock.bind(('', port))

        server_thread=ServerThread(sock,port)
        server_thread.start()

        print("Le serveur est en service...")
        while True:
                
                try:
                	menu()
                        choix=input(">>")
                        if choix==1:
                                break
                        elif choix==0:
                        	nbr=len(server_thread.clients)
                        	if nbr==0:
                        		print 'aucun client n\'est connecte pour le moment'
                        	else:
                        		print 'Les %s clients connectes au serveur sont: '%nbr
                        		for addr in server_thread.clients:
                        			ip,port=addr
                        			print '%s:%s'%ip %port
                        		
                except(TypeError,ValueError):
                        print("choix doit etre un entier")
        server_thread.shutdown()

        server_thread.join()
        print "Le serveur s'est arrete normalement!"
except socket.error as e:
        print "Erreur "+e.message
except Exception as e:
        print "Erreur inconnue "+e.message
finally:
        sock.close()
