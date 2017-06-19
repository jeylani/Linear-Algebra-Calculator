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

class ClientThread(threading.Thread):
        def __init__(self,ip,port,client_socket):
                threading.Thread.__init__(self)
                self.ip=ip
                self.port=port
                self.client_socket=client_socket
                print("[+] Nouveau thread pour %s %s" % (self.ip, self.port))
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
                                                print 'Taille de la reponse %s ' %len(response)
                                                #print response
                                                self.client_socket.send(response)
                                except (NameError,TypeError):
                                        self.client_socket.send(json.dumps({'error':"Les valeurs saisies sont incompletes!: "}))				
                                except ZeroDivisionError :
                                        self.client_socket.send(json.dumps({'error':"Imposible de diviser un nombre par zero"}))	
                                except (ValueError):
                                        self.client_socket.send(json.dumps({'error':"L'une des valeurs saisie est invalide!"}))
                                except numpy.linalg.linalg.LinAlgError as msg:
                                        self.client_socket.send(json.dumps({'error':msg.message}))

                except socket.error as msg:
                        print 'Erreur socket:%s'%msg	
                finally:
                        self.client_socket.close()
class ServerThread(threading.Thread):
        def __init__(self,sock):
                threading.Thread.__init__(self)
                self.sock=sock
                self.arret=False
        def run(self):
                threads=list()
                while not self.arret:
                        self.sock.listen(5)
                        (client_socket, (ip,port)) = self.sock.accept()
                        client_thread=ClientThread(ip, port, client_socket)
                        threads.append(client_thread)
                        client_thread.start()
                for thread in threads:
                        thread.join(timeout=1/10)
        def shutdown(self):
                self.arret=True


try:	
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 15555))

        server_thread=ServerThread(sock)
        server_thread.start()

        print("Le serveur est en service...")
        while True:
                print("0: Afficher la liste des clients connectes")
                print("1:Arreter le serveur de facon normal")
                print("2:Forcer l'arret du serveur")
                print("Quel est votre requete?")
                try:
                        choix=input(">>")
                        if choix==1:
                                break
                except(TypeError,ValueError):
                        print("choix doit etre un entier")

        print "Fermeture du serveur"
        server_thread.shutdown()
        server_thread.join(timeout=1.)
except socket.error:
        print "Erreur "
except:
        print "Erreur inconnue"
finally:
        sock.close()
