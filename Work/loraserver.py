#SIMULADOR SERVIDOR LORA APP SERVER

import requests
import time
from numpy import random as rnd
import json


while 1:

	URL = "http://localhost:22404"

	humidity = rnd.randint(100)
	temperature = rnd.randint(low=15, high=28)

	# print(humidity, temperature, device, sep="\n")

	DATA={"base_station":"0E7D", "temperature":temperature,"humidity":humidity}

	print("¿Desea enviar un dato? 'y' or 'n'") #preguntamos por consola al usuario
	key=input() #leemos teclado

	if key == "y":
		
		response = requests.get(URL, data = json.dumps(DATA))
		print(response)
		print("enviado")
		# time.sleep(10)
			
	else:	
		continue
