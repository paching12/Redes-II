import socket
import select
import json
import threading
import struct
import os, time


def getDic():
	ipv4 = os.popen('ifconfig en0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
	# ipv4 = os.popen('ip addr show eth0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
	# print( ipv4 )
	return ipv4

def sendDirection( ip ):
	# Enviar dirección en multicast
	multicast_group = ('224.3.29.71', 10000)
	while 1:
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.setblocking(0)
		sock.settimeout(0.2)
		# sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
		# sock.sendto(ip.encode(), (MCAST_GRP, MCAST_PORT))
		ttl = struct.pack('b', 1)
		sock.setsockopt( socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl )
		try:
			sent = sock.sendto( ip.encode(), multicast_group )
		except:
			time.sleep(0.1)



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

def reciveDic():
	global a
	a = []
	multicast_group = '224.3.29.72'
	server_address = ('', 9998)
 	# Create the socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setblocking(0)

	# Bind to the server address
	sock.bind(server_address)
	group = socket.inet_aton(multicast_group)
	mreq = struct.pack('4sL', group, socket.INADDR_ANY)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
	sock.settimeout( 2 )
	data = json.loads( recvall( sock ) )
	a = data 
	print( 'valor a:', a )
	sock.close()

def reflectCopy():
	multicast_group = '224.0.0.2'
	server_address = ('', 9997)
	# while 1:
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind( server_address )
	ttl = struct.pack('b', 1)
	sock.setsockopt( socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl )
	sock.setblocking(0)
	sock.settimeout(0.2)
	data = json.dumps(a)
	try:
		print('sync')
		sent = sock.sendto( data.encode(), multicast_group )
	except:
		time.sleep(0.2)

def option( socket, option ):
	if option == '1':
		data = json.dumps(a)
		socket.sendall( data.encode() )
		print( 'valor a:', a )
		print( 'Enviando diccionario' )
	elif option == '2':
		# recibir nuevamente
		print( 'Modo de inserción ')
		data = recvall( socket )
		print( 'insertando...' )
		data = data.decode()
		a.append(data)
		reflectCopy()

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
			print( 'Ocurrió un error' )
		# print( 'index:' , index )
	else: print( 'opción desconocida', option )

def runServer():
	server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.bind( (getDic(), 9999) )
	server.listen( 3 )

	toread = [server]

	running = 1
																																																				   
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
					print( "Desconexión de cliente" )
					s.close()

					# remove socket so we don't watch an invalid 
					# descriptor, decrement client count                                                                                                                                                                      
					toread.remove( s )
					# running = len(toread) - 1
# runServer()
# try:
threading.Thread( target=reciveDic ).start()
threading.Thread( target=sendDirection, args=(getDic(),) ).start()
threading.Thread( target=runServer ).start()
# except:
#    print ("Error: unable to start thread")
