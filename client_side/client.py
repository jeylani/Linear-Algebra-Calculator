#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 08:29:14 2017

@author: jeylani
"""
import socket
import json
import threading
import time

class ClientTCP(threading.Thread):
	def __init__(self,host,port,callback):
		threading.Thread.__init__(self)
		self.sock=socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, _sock=None)
		self.sock.connect((host,port))
		self.msg="Connection on {}".format(port)
		self.callback=callback
		self.job=False
		self.arret=False
	def set_operation(self,operator,operandes):
		self.operator=operator
		self.operandes=operandes
		self.job=True
	def run(self):
		while not self.arret:
			if self.job:
				request=json.dumps({'operateur':self.operator,'operandes':self.operandes})
				self.sock.send(request)
				response=self.sock.recv(1024)
				result=json.loads(response)
				
				time.sleep(0.03)
				self.callback(result)
				self.job=False
	def disconnect(self):
		self.arret=True
		self.sock.send('{"operateur":"DISCONNECT"}')
	def close(self):
		self.sock.close()

def afficher(result):
	print result

"""client=ClientTCP('127.0.0.1', 15555,afficher)
client.start()
#print "Lancement du thread termine attente d'une reponse"

try:
	
	while True:
		
		operateur=input("Quel est l'operateur : ")
		
		if operateur=='DISCONNECT':
			print("Fermeture du client")
			client.disconnect()
			break
		else:
			operandes=input("Donner la liste des operandes separees par des virgules: ")
		
			result=client.set_operation(operateur, operandes)
			
except socket.error as e:
	print "Erreur socket (%s)"%e
finally:
	if 'client' in globals():
		client.close()
		"""
	
