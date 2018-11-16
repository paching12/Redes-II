import sys, os
import socket
import struct
import json
from time import sleep

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

def chooseServer():
	multicast_group = '224.3.29.71'
	server_address = ('', 10000)

	# Create the socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	# Bind to the server address
	sock.bind(server_address)
	group = socket.inet_aton(multicast_group)
	mreq = struct.pack('4sL', group, socket.INADDR_ANY)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

	ip = recvall( sock )
	ip = ip.decode()
	sock.close()
	return ip

def imprimirLista( data ):
	i = 1
	for item in data:
		print( i,'.-',item )
		i += 1

def option( socket, opcion ):
	s.send(opcion.encode())
	if opcion == '1':
		data = json.loads( recvall( socket ) )
		imprimirLista( data )
		input( 'presione enter para continuar' )
		os.system( 'clear' )
	elif opcion == '2':
		nombre = input('Ingrese un nombre:');
		socket.send(nombre.encode('utf-8'))
	elif opcion == '3':
		data = json.loads( recvall( socket ) )
		imprimirLista( data )
		index = input( 'Ingrese el número de elemento que desea eliminar: ')
		try:
			socket.send(index.encode())
		except:
			print( 'número no válido' )
		finally:
			os.system( 'clear' )
	else: print( 'opción desconocida', option )

try:
	ip = chooseServer()
	# ip = '192.168.1.73'
	print('ip', ip)
	opcion  = ''
	while( opcion not in ['1','2','3', '4'] ):
		opcion = input('''1.- Ver diccionario
2.- Añadir al diccionario
3.- Eliminar del diccionario
4.- Salir
''');
		os.system( 'clear' )
		if opcion != '4':
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect((ip,9999))
				option( s, opcion )
			except(socket.error):
				print ("Error al conectar")
			finally:
				opcion = ''
				s.close()
except:
	print('No hay servidores disponibles')

