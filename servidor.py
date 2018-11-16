#!/usr/bin/python                                                                                                                                                                                                                                                    

import socket
import select
import threading
import json

server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind( ('localhost', 10000) )
server.listen( 3 )
server.setblocking(0)

toread = [server]

running = 1

a = [ 'Jose' ]

def sendList():
	MCAST_GRP = '224.1.1.1'
	MCAST_PORT = 5007
	while 1:
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
			sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
			sock.sendto('Hello World!'.encode(), (MCAST_GRP, MCAST_PORT))
			print( "Enviando copia vía multicast" )
		except:
			print( "No es posible enviar copiar de la lista" )

def recvall(sock):
    BUFF_SIZE = 1024 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data

def option( socket, option ):
	if option == '1':
		data = json.dumps(a)
		socket.sendall( data.encode() )
		print( 'Enviando diccionario' )
	elif option == '2':
		# recibir nuevamente
		print( 'Modo de inserción ')
		data = recvall( socket )
		print( 'insertando...' )
		data = data.decode()
		a.append(data)	

	elif option == '3':
		# recibir nuevamente
		data = json.dumps(a)
		socket.sendall( data.encode() )
		print( 'Eliminando... ')
		index = recvall( socket )
		index = index.decode()
		try:
			index = int(index) - 1
			del a[index]
		except:
			print( 'index inválido' )
		print( 'index:' , index )
	else: print( 'opción desconocida', option )

def runServer():
	while 1:
		rready,wready,err = select.select( toread, [], [] )
		for s in rready:
			if s == server:
				# accepting the socket, which the OS passes off to another                                                                                                                                                                                               
				# socket so we can go back to selecting.  We'll append this                                                                                                                                                                                              
				# new socket to the read list we select on next pass                                                                                                                                                                                                     

				client, address = server.accept()
				toread.append( client )  # select on this socket next time                                                                                                                                                                                               
			else:
				# Not the server's socket, so we'll read                                                                                                                                                                                                                 
				data = s.recv( 1024 )
				if data:
					print( "Received %s" % ( data  ) )
					option( s, data.decode() )
				else:
					print( "Client disconnected" )
					s.close()

					# remove socket so we don't watch an invalid 
					# descriptor, decrement client count                                                                                                                                                                      
					# toread.remove( s )
					# running = len(toread) - 1

	# clean up                                                                                                                                                                                                                                                           
	server.close()


sendList()
# try:
# 	# threading.Thread(target=runServer).start()
# 	# threading.Thread(target=).start()
# except:
#    print ("Error: unable to start thread")