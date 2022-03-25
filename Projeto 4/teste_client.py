from protocol import Protocol
from enlace import Enlace

import numpy as np
import time
import sys

SERIAL_PORT_NAME = "/dev/cu.usbmodem14401"

# criação das instâncias de Enlace e Protocol
com = Enlace(SERIAL_PORT_NAME)
com.enable()

try:

	# ---
	time.sleep(0.2)
	com.fisica.flush()
	protocol = Protocol(com)

	# byte de sacrifício
	print("\nEnviando 1 byte de sacrifício...")
	com.sendData(b'\x01')
	print("OK\n")
	time.sleep(2)

	'''
	TEMPLATES

	1: [b'\x01', b'\xAA', b'\xAA', b'\x01', b'\x01', 'server_id', b'\x00', b'\x00', b'\xAA', b'\xAA'],
	2: [b'\x02', b'\xAA', b'\xAA', b'\x01', b'\x01', 'client_id', b'\x00', b'\x00', b'\xAA', b'\xAA'],
	3: [b'\x03', b'\xAA', b'\xAA', 'number_of_packets', 'packet_id', 'payload_size', b'\x00', b'\x00', b'\xAA', b'\xAA'],
	4: [b'\x04', b'\xAA', b'\xAA', b'\x01', b'\x01', b'\x00', b'\x00', 'last_successful_packet', b'\xAA', b'\xAA'],
	5: [b'\x05', b'\xAA', b'\xAA', b'\x01', b'\x01', b'\x00', b'\x00', b'\x00', b'\xAA', b'\xAA'],
	6: [b'\x06', b'\xAA', b'\xAA', b'\x01', b'\x01', b'\x00', 'wanted_packet', b'\x00', b'\xAA', b'\xAA']

	'''

	# definição do pacote de teste
	print('Pacote:')
	eop_pacote = [b'\xAA', b'\xBB', b'\xCC', b'\xDD']
	head_pacote = [b'\x05', b'\xAA', b'\xAA', b'\x01', b'\x01', b'\x00', b'\x00', b'\x00', b'\xAA', b'\xAA']
	dados_pacote = head_pacote + [b'\xD3'] * 0 + eop_pacote
	print(dados_pacote, end='\n\n')

	# envio de pacote teste
	print('Enviando pacote de teste...')
	com.sendData(np.asarray(dados_pacote))
	print("OK\n")

	com.disable()
	sys.exit()

except Exception as error:
	com.disable()
	raise error








