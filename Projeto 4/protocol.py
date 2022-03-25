
from time import time
from packet import Packet
from enlaceRx import RX

import utils

class Protocol:
	'''
	Representa o protocolo de comunicação a ser implementado
	no projeto 4.

	'''

	class ProtocolError(Exception): pass
	class HeadError(ProtocolError): pass
	class TimeoutError(ProtocolError): pass
	class PayloadError(ProtocolError): pass
	class MissingDataError(ProtocolError): pass


	def __init__(self, com):
		''' Cria uma nova instância de Protocol '''
		
		# amarra o enlace "com" ao protocolo
		self.com = com
	

	def getPacketInfo(self, time_limit=5):
		''' Chama getData para o tamanho do head e retorna um dicionário com dados relevantes '''

		# dicionário de retorno
		message_info = dict()

		# chama getData
		try: data = self.com.getData(Packet.HEAD_SIZE, time_limit=time_limit)
		except RX.RXTimeoutError: raise Protocol.TimeoutError('Timeout na recepção da mensagem')
		except RX.RXNotEnoughDataError: raise Protocol.HeadError('Não foram recebidos dados o suficiente')

		# converte os dados recebidos a uma lista de bytes
		bytes_list = utils.splitBytes(data)

		# extrai o tipo da mensagem do head e extrai o template relevante
		message_type = int.from_bytes(bytes_list[0], byteorder='big')
		message_info['type'] = message_type
		try: head_template = Packet.HEAD_TEMPLATES[message_type]
		except KeyError: raise Protocol.HeadError('Tipo de mensagem inválido')

		# verifica a validade byte a byte
		for index in range(Packet.HEAD_SIZE):

			# extrai o byte esperado e o recebido das listas
			expected = head_template[index]
			received = bytes_list[index]

			# se o valor esperado for uma string, finalizar iteração
			if isinstance(expected, str):

				value = int.from_bytes(received, byteorder="big")

				# verifica a validade do tamanho do payload
				if expected == 'payload_size':
					if value > 114: raise Protocol.HeadError('Tamanho do payload grande demais')

				# verifica a validade do id do pacote
				if expected == 'packet_id':
					number_of_packets = message_info['number_of_packets']
					if value > number_of_packets: raise Protocol.HeadError('Número do pacote é maior que a quantidade total de pacotes')

				message_info[expected] = value

			# verifica se o valor é o esperado
			elif expected != received: raise Protocol.HeadError('Byte %d do HEAD inválido' % (index + 1))

		return message_info

	
	def getPayload(self, message_info):
		''' Chama getData para o tamanho do payload especificado num head já recebido com getMessageInfo '''

		# extrai o tamanho do payload esperado
		message_type = message_info['type']
		payload_size = Packet.MESSAGE_TYPE_PAYLOAD_SIZE[message_type]

		# caso variável, extrair do HEAD
		if payload_size == 'variable': payload_size = message_info['payload_size']
		print('Expected payload size: %d' % payload_size)

		# extrai os dados e limpa o buffer
		try: data = self.com.getData(payload_size + Packet.EOP_SIZE, time_limit=1)
		except RX.RXTimeoutError: raise Protocol.MissingDataError('Dados recebidos foram deletados entre as chamadas de Protocol.getMessageInfo e Protocol.getPayload')
		except RX.RXNotEnoughDataError: raise Protocol.PayloadError('Tamanho de payload menor que o esperado')
		self.com.rx.clearBuffer()

		# formata os dados e extrai o EOP e o payload
		data = utils.splitBytes(data)
		payload = data[ : -1 * Packet.EOP_SIZE]
		eop = data[-1 * Packet.EOP_SIZE:]

		# verifica se o EOP é valido
		if eop != Packet.EOP_LIST: raise Protocol.PayloadError('Tamanho de payload maior que o esperado')

		# retorna a lista de bytes do payload
		return payload





