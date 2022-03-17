'''
Protocolo de comunicação.

Define coisas como os dados do handshake, etc.

'''

import utils
import numpy as np

from pacote import Packet
from mensagem import Message

# o handshake são 2 bytes fixos nas pontas e alguns no meio
# para indicar a quantidade de pacotes a serem transmitidos
HANDSHAKE_TEMPLATE = [b'\xAB'] + Packet.NUMBER_SIZE * ['ammount'] + [b'\xAB']

# respostas do servidor
PACKET_ERROR_DATA = [b'\x38'] * Packet.PAYLOAD_SIZE		# indica erro
PACKET_RECEIVED_DATA = [b'\xD2'] * Packet.PAYLOAD_SIZE	# indica êxito


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

RANDOM_DATA = [b'\xad', b'\x89', b'\xa9', b'9', b'\x04', b'\x89', b'\x7f', b'<', b'>', b'\x9a', b'\xfc', b'\xdf', b'I', b'W', b',', b'\xa9', b'\xae', b'~', b'p', b'x', b'A', b'2', b'B', b'<', b']', b'\xd4', b'\xdd', b'\xde', b'\x82', b'\x1d', b'\xfb', b'\xce', b'\x14', b'u', b'U', b'\x82', b'k', b'\xdd', b'\xf9', b'\xf9', b'\r', b'M', b'g', b'\x9e', b'e', b'\xe0', b'\xe2', b'\xbb', b'\x9b', b'\xe5', b'\x0b', b'\xca', b'\x91', b'\xfa', b'"', b'\xa4', b'\xd0', b'\x8e', b'\xd8', b'E', b'\xeb', b'\xde', b'\xfe', b'F', b'\x10', b'\xd1', b'\xc9', b'\t', b'\xea', b':', b'6', b'\xe5', b'\x1b', b'K', b'I', b'{', b'\xc0', b'\xc9', b'\xc6', b'\x01', b'\xf8', b'\xcc', b'\xf0', b'y', b'\xdd', b'\x0e', b'\xba', b'3', b';', b'\x88', b'\xbc', b'\x18', b'\x01', b'\x15', b'\x9b', b'\x83', b'\xc9', b'\x88', b'Z', b'k', b'\x92', b'l', b'\xe4', b'#', b'x', b'&', b'\xf6', b'\xc6', b'W', b'\xc4', b'X', b'\xd3', b'1', b'f', b'\xbe', b'\xe5', b'\xe1', b'Z', b'\x9d', b'\x14', b'\xad', b'/', b'\x83', b'Q', b'\x15', b'\xc5', b'\x9c', b'\xed', b'\xff', b'H', b'\xf4', b'\xef', b'\x80', b'S', b'\xf4', b'\xf7', b'\xc4', b'\x9e', b'\xf4', b'\x7f', b'7', b'\x98', b'\xf9', b'&', b'.', b'\x81', b'7', b'e', b'|', b'\xb5', b'\xac', b'5', b'/', b'\xe3', b'\xc2', b'*', b'5', b'Y', b'\x9f', b'\xe7', b'\xa1', b'\xd6', b'\xb3', b'\x9b', b'}', b'\x81', b'&', b'\xa1', b'\x8d', b'\x1c', b'\x90', b'\xe2', b'\x92', b'y', b'\xb9', b'\xbb', b'>', b'~', b';', b'\x94', b'\xa9', b'\xfb', b'\xf9', b'\x97', b'\x05', b'\xce', b'\xd6', b'\xa3', b'\x91', b'A', b'\x89', b'W', b'\xf3', b'B', b'+', b'\xff', b'\xbf', b'H', b'\xa7', b'\xc2', b'\xd8', b'\x85', b'\xae', b'{', b'\x85', b'D', b'\xa3', b'\xb6', b'\xf0', b'M', b'!', b'\x8c', b'\x98', b'@', b'(', b'\xe9', b'\xb1', b'\x84', b'\x99', b'\xb7', b'\xf3', b'\x93', b'j', b'\xdc', b'Y', b'C', b'X', b'\xdc', b'\xfd', b'W', b'\xed', b';', b'\xe5', b'\\', b'\x10', b'I', b'\x08', b'J', b'S', b'p', b'.', b'q', b'\xde', b'\xdc', b'\x9c', b'\xd4', b'\xcc', b'!', b'q', b'\xd0', b'F', b'J', b'\xd2', b'\xa7', b'\x93', b'\xf7', b'\x95', b'i', b'K', b'B', b'\xdb', b'0', b'\xef', b'\xd9', b'\xb4', b'S', b'\x93', b'\x89', b'$', b'j', b'\xe4', b'\xea', b'\x19', b'\x10', b'|', b'\xf0', b'\x1b', b'\xa8', b'\xcd', b'E', b'\x83', b'K', b'\x9c', b'\xe2', b'\xde', b'X', b'\x96', b'<', b'f', b'e', b' ', b'\xab', b'\x83', b'\x92', b'\xf2', b'\xd3', b'\x16', b'`', b'\xa2', b'\xab', b'\xf5', b'\xf9', b'#', b'\x8c', b'\xbd', b'v', b'O', b'\xc6', b'\xbd', b'n', b'\x89', b'\xef', b'\x1f', b'\xdc', b'\xc1', b'y', b'\xfa', b'\xe8', b'U', b'0', b'Q', b'\x19', b'\x14', b'\xc9', b'p', b'\x9b', b'}', b'\x19', b'-', b'h', b'7', b'.', b'\xad', b'\x93', b':', b'\xc8', b'o', b'\x17', b'\xa8', b'\r', b'\xe9', b'\x8c', b'(', b'\xb1', b'\x9b', b'6', b'x', b'\x1f', b'\xde', b'E', b'[', b'8', b'\x86', b'\x05', b'Q', b'K', b'\xb1', b'p', b'\x9e', b't', b'u', b'G', b'\xe9', b'\xab', b'\xf8', b'\xa8', b'L', b'\xf2', b'R', b'\xc8', b'\xe7', b'\x15', b'\x96', b'\xfe', b'\xa1', b'\x0c', b'\xa8', b'\xc6', b'\xe6', b'u', b'\xd4', b'\x18', b'\x15', b'\x83', b'\xe1', b'\xe9', b'\xd1', b'\x83', b'\xee', b'\xa6', b'`', b'<', b'\xea', b'\x9a', b',', b'\xa6', b'\xcb', b'\xd7', b'=', b'\x17', b'\x7f', b'D', b'e', b'p', b'`', b'\xab', b'Q', b'\xdc', b'\xe1', b'.', b'\xe5', b'\x81', b'\x1a', b'\xe9', b'y', b'Y', b'\xc4', b'w', b'\\', b'\xca', b'\xa0', b'@', b'\x85', b'\xe8', b'\x92', b'%', b'.', b'\xab', b'\xb0', b'\xf2', b'\xdd', b'\xe9', b'\x9f', b'\t', b'D', b'\xe6', b'y', b'\x8a', b'(', b'$', b'n', b'g', b'\xb1', b'\xca', b'\x9d', b'Q', b'o', b'\x9e', b'l', b'\x15', b'W', b'\x14', b'\xc0', b'\xcc', b'\xf9', b'\xd5', b'r', b'\xf0', b'\xa4', b'0', b'l', b'\x8f', b'\x91', b'\xb5', b'[', b'\x8d', b'\x92', b'@', b'\xfc', b'\xdd', b'\xca', b'W', b'\x84', b'\xf5', b'\xaf', b'R', b'\xf7', b'p', b'\x9e', b'\xab', b'\xd9', b'\xb9', b'F', b'\xe6', b'\x05', b'\xd4', b' ', b'\xaa', b'\xaa', b'l', b'4', b'\xd6', b'\x07', b'\xd0', b')', b'\xad', b'\xb7', b'\xb4', b'\xa2', b'7', b'\xda', b'\x94', b'N', b'\xc3', b'Z', b'\x0c', b'~', b'J', b'P', b'\xad', b'#', b'\xba', b'\xa3', b'S', b'\x89', b'v', b'6', b'\x9b', b'$', b'\x06', b'\x84', b'8', b'\x1c', b'\x99', b'\xa3', b'G', b'\xb3', b'\xb0', b'\x06', b'\x89', b'\x01', b'T', b'\xd5', b'6', b'\x9a', b'&', b'\xac', b'\xfd', b'X', b'\xe4', b'\xd9', b"'", b't', b'\x10', b'\xfe', b'H', b'\xf1', b'=', b'\xca', b'\xb5', b'\xb5', b'\xf4', b'P', b'\xa2', b'\x9c', b'\xe7', b'\xa3', b'\xff', b'\xc4', b'@', b'm', b'\x92', b'\x82', b'\xcb', b'\xa2', b'1', b'\xe9', b'\xc5', b'\xd4', b'\x9f', b'\xd1', b'b', b'\xbc', b'Y', b'\x9b', b'\x18', b'\xad', b'A', b'j', b'\xfb', b'\x8a', b'\xea', b'\xda', b'\x97', b'\x14', b'\xb7', b'\xeb', b'F', b'\xff', b'v', b'U', b'\x89', b'\xcd', b'\xee', b'i', b'\\', b'\xed', b'"', b'\xcf', b'w', b'\xad', b'\x89', b'U', b'w', b'\x1e', b'^', b'U', b'\xf7', b'N', b'_', b'L', b'u', b')', b'C', b'q', b'\xb7', b'c', b'\xf2', b'\xd5', b'\xcd', b'I', b'\x9b', b':', b'\x83', b'\xe7', b'\x14', b'\xc1', b'B', b'O', b'\x96', b'\x0e', b'q', b'\x8a', b'\x9a', b'\xfb', b'\x7f', b'h', b'\xae', b'\xc4', b'\xc1', b'\xb0', b'\xe7', b'\xe5', b':', b'H', b'\x98', b'\x03', b'5', b'\x12', b'c', b's', b'\xbd', b'\x80', b'\x86', b'\t', b'{', b'\xfb', b'\xf9', b'r', b'\x04', b'\xd2', b'2', b'\x1d', b'\xdb', b'\xd0', b'V', b'\xd1', b'\xff', b'\xf7', b'\xe6', b'p', b'1', b'\xa5', b'\xa9', b'\xcc', b'\x11', b'\xc7', b'\xc1', b'\xf3', b'\xa3', b'\xd6', b'\xf4', b'\x9d', b'\xe0', b'\xff', b'\x8f', b'\xa6', b'_', b'e', b'i', b'(', b'w', b'\xbd', b'\xc3', b'g', b'\x9f', b'\x04', b'\xcd', b'\x7f', b'2', b'u', b'\x13', b'>', b'\xeb', b'\x8b', b'\x18', b'\x89', b'\xb6', b'9', b'\x95', b'\xd7', b'\x89', b'\xee', b'=', b'I', b'\xd8', b'\x00', b'V', b'\xd8', b'b', b'\x96', b'\x92', b'9', b';', b'P', b'\xdc', b'}', b'\x07', b'\xda', b'e', b'\\', b'\xcf', b'\x93', b'\xb7', b'3', b'\x83', b'!', b'T', b'X', b'\x19', b'\x11', b'\xd2', b'\x00', b'\x14', b'4', b'\xe8', b'\x9d', b'\xe3', b'\x05', b'\x17', b'\xe3', b'o', b'\xe2', b'>', b'\x17', b'W', b'\xfe', b'\x1c', b'\x07', b'\xc1', b'\xfd', b'\x98', b'\x85', b'O', b'\xbf', b'\x0b', b'\xc3', b'\n', b'[', b'\xfb', b'!', b'"', b'\xbf', b'\x05', b'<', b'F', b'y', b'\xc7', b'&', b'm', b'^', b'Q', b'9', b'\x16', b'\xe9', b'\x7f', b'\x1c', b'\xe0', b'\xca', b'\x85', b'\xe6', b'!', b'9', b'\x91', b'G', b'\xb5', b'\xcb', b'\xa5', b'_', b'\x83', b'\xfb', b'\xec', b'D', b'>', b'\xcc', b'\xaa', b'v', b'\xe9', b'9', b'\xe5', b'\xd7', b'F', b'\xc9', b'\xb7', b'\xb5', b'\xb7', b'\xdc', b'A', b'\xdf', b'N', b')', b':', b'\x1b', b'\x0f', b'\xc6', b'v', b'7', b'U', b')', b'\xe7', b'\x86', b',', b'J', b'0', b'\xd5', b'\x8c', b'\xd7', b'\x95', b'\xef', b'\xc0', b'\x12', b'\xa2', b'o', b'\xc7', b'\xe3', b'\xc3', b'r', b'\xcf', b'\x89', b'\xff', b'i', b"'", b'\xb0', b'\xe5', b'\xde', b'\xfb', b'\x11', b'\x91', b'\xb8', b'\x8e', b'\x16', b'.', b'\x8b', b'\x0b', b'|', b'1', b'\xea', b'\xe5', b'\x0c', b'C', b'3', b'=', b'\xcb', b'\xc9', b'T', b'\x82', b'w', b'\x87', b'\xec', b'\xca', b'm', b'\xeb', b'y', b'\xdf', b'\x92', b'T', b'\x9d', b'\xd9', b'{', b'\xf1', b'\x7f', b'\x7f', b'~', b'\x1a', b'\x06', b'\xa8', b'G', b'\xfe', b'\xf9', b'\xac', b'\x0c', b'\xcc', b'8', b'r', b'\xe1', b'\xe0', b'\x81', b'\xc9', b'\xd5', b'\xfd', b'\xa6', b'\xc6', b'\x03', b'\x8f', b'8', b'\x9d', b'\xe8', b'\xee', b'\xfb', b'\x8c', b'5', b'\xe6', b'\x05', b'u', b'3', b'\x12', b'\xa5', b'\xb9', b'k', b'\x92', b'\x17', b'\x16', b'w', b'\xb2', b'\xf4', b"'", b' ', b'\xb1', b'\x13', b'\xd0', b'\xe1', b'\n', b'\xc8', b'\xac', b'\xa0', b'\x88', b'9', b'\xeb', b'\xf7', b'\t', b'q', b':', b'\x1a', b'\xf0', b'\x9b', b'\x02', b'u', b'\x9b', b'\xb1', b'\x1d', b'\x17', b'\x18', b'\xc4', b'\xc8', b'\x93', b'\xad', b'\xdd', b',', b'z', b'p', b'^', b'\xaa', b'\xf0', b'\xba', b'\xf2', b'\xf5', b'\x1a', b'\xca', b'o', b'\x17', b'h', b'\xc1', b'\x0b', b'P', b'\x9d', b'\n', b'\x80', b'\xc4', b'\xd8', b'\x07', b'\x88', b'\xc2', b'\x8c', b'\xcb', b'W', b'\xec', b'\x0c', b'[', b'\xb7', b'T', b'\xc3', b'\xbe', b'\xc0', b'\xe1', b'\x0b', b'\xa6', b't', b'v', b'\xc8', b'\xad', b'X', b'\xd2', b'*', b'f', b'R', b'\x89', b'\xcb', b'\xc3', b'v', b'_', b'\xbe', b'\x93', b's', b'\x87']








