from protocol import Protocol
from enlace import Enlace

import time
import sys

SERIAL_PORT_NAME = "/dev/cu.usbmodem14201"

try:

	# criação das instâncias de Enlace e Protocol
	com = Enlace(SERIAL_PORT_NAME)
	com.enable()
	time.sleep(0.2)
	com.fisica.flush()
	protocol = Protocol(com)

	# byte de sacrifício
	print("\nEsperando 1 byte de sacrifício...")
	rxBuffer = com.getData(1, time_limit=1e12)
	com.rx.clearBuffer()
	print("OK\n")
	time.sleep(.5)

	# teste do Protocol.getMessageInfo
	print('Aguardando pacote de teste...')
	message_info = protocol.getPacketInfo(time_limit=10)
	print("OK\n")
	print(message_info)

	# teste do Protocol.getPayload
	print('Lendo payload...')
	payload = protocol.getPayload(message_info)
	print("OK\n")
	print(payload)
	print()

	com.disable()
	sys.exit()

except Exception as error:
	com.disable()
	raise error


