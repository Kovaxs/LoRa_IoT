# Servidor HTTP

import socket
import requests
import json
from influxdb import InfluxDBClient
from datetime import datetime
from pytz import timezone
import traceback
from numpy import random as rnd

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

device_list = ["0001", "0002", "0003"]

client = InfluxDBClient(host="localhost", port=8086)
try:
	# client.create_database("lora_db")
	# client.get_list_database() 
	client.switch_database("lora_db")
except:
	print("Exepction!!")

#la ip es local host y se especifica con dos comillas '' (por defecto localhost)
s.bind(('',22404))

s.listen(10) #numero máximo de peticiones simultáneas para el servidor


try:
	while 1:
		print("esperando a recibir dato")
		conn, addr=s.accept()
		print("dato recibido")
		print("\n")
		head=conn.recv(1024) #Obtenemos los datos de cabecera en formato bytes
		# print(head)

		body=conn.recv(1024) #Obtenemosv el payload del mensaje en formato bytes
		# print(body)
		data = body.decode('utf-8')
		print(data)

		device = rnd.choice(device_list)
		# data = data.split("&")
		# print(data)
		# data = dict([i.split("=") for i in data])
		# data['temperature'] = int(data['temperature'])
		# data['humidity'] = int(data['humidity'])
		# print(data)
		time_zone = timezone('America/Santiago')
		time = datetime.now(time_zone)

		body_json = [
			{
			"measurement":  "device_" + "0003",
			"tags": {
				"host": "Oleksandr",
				"region": "Murcia"
			},
			"time": time,
			"fields": json.loads(data)
			}]
		print(body_json)
		client.write_points(body_json)


		#ENVIAMOS RESPUESTA AL SERVIDOR
		#es obligatorio enviar una respuesta ya que el cliente se queda bloqueado esperandola
		r_protocol='HTTP/1.1'.encode()
		r_status='200'.encode()
		r_status_text='OK'.encode()
		conn.send(b'%s %s %s' %(r_protocol, r_status, r_status_text))
		print("Sent")

		conn.close() #cierre de la comunicacion


except:
	print("Ha ocurrido una excepcion")

finally:
	conn.close()
	s.close()

