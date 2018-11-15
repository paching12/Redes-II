#!/usr/bin/python                                                                                                                                                                                                                                                    

import socket
import select
import json

server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind( ('localhost', 10000) )
server.listen( 3 )

toread = [server]

running = 1

a = [ 'Jose' ]

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

# we will shut down when all clients disconenct                                                                                                                                                                                                                      
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
				toread.remove( s )
				running = len(toread) - 1

# clean up                                                                                                                                                                                                                                                           
server.close()

# import socket
# import json
# from threading import *


# HOST = '127.0.0.1'                 # Symbolic name meaning the local host
# PORT = 10000 
# # serversocket.bind((host, port))
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((HOST, PORT))
# a = { 'id': '1234' }


# class client(Thread):
# 	def __init__(self, socket, address):
# 		Thread.__init__(self)
# 		self.sock = socket
# 		self.addr = address
# 		self.start()

# 	def run(self):
# 		while 1:
# 			data = self.sock.recv(1024).decode()
# 			print('Client sent:', data )
# 			self.option( data )
# 			break

# 		self.sock.close()
# 			# self.sock.send(b'Oi you sent something to me')

# 	def option( self, option ):
# 		if option == '1':
# 			data = json.dumps(a)
# 			self.sock.sendall( data.encode('utf-8') )
# 			print( 'Enviando ', data )
# 		elif option == '2':
# 			# recibir nuevamente
# 			print( 'Añadiendo ')
# 		elif option == '3':
# 			# recibir nuevamente
# 			print( 'Editando ')

			

# s.listen(3)

# print ('server started and listening')
# while 1:
# 	conn, addr = s.accept()
# 	print( 'Connected by', addr )
# 	client(conn, addr)