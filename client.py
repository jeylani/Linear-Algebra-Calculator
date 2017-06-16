#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 08:29:14 2017

@author: jeylani
"""
import socket
import json

class ClientTCP():
	def __init__(self,host,port):
		self.sock=socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, _sock=None)
		self.sock.connect((host,port))
		self.msg="Connection on {}".format(port)
	def send_operation(self,operateur,operandes):
		request=json.dumps({'operateur':operateur,'operandes':operandes})
		self.sock.send(request)
		response=self.sock.recv(255)
		result=json.loads(response)
		return result
	def disconnect(self):
		self.sock.send('{"operateur":"DISCONNECT"}')
	def close(self):
		self.sock.close()
try:
	client=ClientTCP('127.0.0.1', 15555)	
	while True:
		
		operateur=input("Quel est l'operateur : ")
		
		if operateur=='DISCONNECT':
			print("Fermeture du client")
			client.disconnect()
			break
		else:
			operandes=input("Donner la liste des operandes separees par des virgules: ")
		
			result=client.send_operation(operateur, operandes)
			if 'error' in result:
				print('ERREUR:%s'%result['error'])
			elif 'result' in result:
				print("Le resultat du calcul:%s" %result['result'])
except socket.error as e:
	print "Erreur socket (%s)"%e
finally:
	if 'client' in globals():
		client.close()