import sys, os
import socket
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
			s.connect(('127.0.0.1',10000))
			option( s, opcion )
		except(socket.error):
			print ("Error al conectar")
		finally:
			opcion = ''
			s.close()
