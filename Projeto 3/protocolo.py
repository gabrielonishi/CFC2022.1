'''
Protocolo de comunicação.

Define coisas como os dados do handshake, etc.

'''

import utils

from pacote import Packet
from mensagem import Message

# o handshake são 2 bytes fixos nas pontas e alguns no meio
# para indicar a quantidade de pacotes a serem transmitidos
HANDSHAKE_TEMPLATE = [b'\xAB'] + Packet.NUMBER_SIZE * ['ammount'] + [b'\xAB']

# respostas do servidor
PACKET_ERROR_DATA = [b'\x38']		# indica erro
PACKET_RECEIVED_DATA = [b'\xD2']	# indica êxito


def buildHandshake(message):
	''' Retorna uma lista de bytes que são os dados do handshake '''

	ammount = message.number_of_packets

	number_of_packets_bytes = ammount.to_bytes(Packet.NUMBER_SIZE, byteorder="big")
	number_of_packets_bytes = utils.splitBytes(number_of_packets_bytes)

	handshake_data = list()
	index_to_add = 0

	for component in HANDSHAKE_TEMPLATE:

		if isinstance(component, str):
			handshake_data.append(number_of_packets_bytes[index_to_add])
			index_to_add += 1

		else: handshake_data.append(component)

	return handshake_data


def validateHandshake(message):
	''' Retorna se uma mensagem é um handshake válido '''

	ammount_bytes = list()

	# verifica a validade dos dados dentro do payload e os extrai
	for i in range(message.data_size):

		expected_value = HANDSHAKE_TEMPLATE[i]
		received_byte = message.data_list[i]

		# lida com bytes variáveis
		if isinstance(expected_value, str):
			ammount_bytes.append(received_byte)

		# lida com bytes fixos
		elif received_byte != expected_value: return (False, None)

	ammount_bytes = b''.join(ammount_bytes)
	ammount = int.from_bytes(ammount_bytes, byteorder="big")

	return (True, ammount)














