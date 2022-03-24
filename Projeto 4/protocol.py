
from time import time
from packet import Packet
import utils

class Protocol:
	'''
	Representa o protocolo de comunicação a ser implementado
	no projeto 4.

	'''

	class ProtocolError(Exception): pass
	class TimeoutError(ProtocolError): pass
	class HeadError(ProtocolError): pass
	class PayloadError(ProtocolError): pass


	def __init__(self, enlace):
		''' Cria uma nova instância de Protocol '''
		
		# amarra o enlace ao protocolo
		self.enlace = enlace
	

	def getHead(self, time_limit):
		''' Chama getData para o tamanho do head e retorna um dicionário com dados relevantes '''

		# dicionário de retorno
		head_info = dict()

		# chama getData, gera um erro de Timeout caso dê timeout
		data, nRx = self.enlace.getData(Packet.HEAD_SIZE, time_limit=time_limit)
		if data is None: raise Protocol.TimeoutError()

		# converte os dados recebidos a uma lista de bytes
		bytes_list = utils.splitBytes(data)

		# extrai o tipo da mensagem do head e extrai o template relevante
		message_type = int.from_bytes(bytes_list[0], byteorder='big')
		head_info['type'] = message_type
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
				if expected == 'payload_size':
					if value > 114: raise Protocol.HeadError('Tamanho do payload inválido')
				head_info[expected] = value

			# verifica se o valor é o esperado
			elif expected != received: raise Protocol.HeadError('Byte %d do HEAD inválido' % (index + 1))

		return head_info

	
	def getPayload(self, head_info):
		''' Chama getData para o tamanho do payload especificado em um head '''

		# extrai o tamanho do payload esperado
		message_type = head_info['type']
		payload_size = Packet.MESSAGE_TYPE_PAYLOAD_SIZE[message_type]

		# caso variável, extrair do HEAD
		if payload_size == 'variable': payload_size = head_info['payload_size']

		# extrai os dados
		data = self.enlace.getData(payload_size + Packet.HEAD_SIZE + Packet.EOP_SIZE)
		data = utils.splitBytes(data)
		payload = data[Packet.HEAD_SIZE : -1 * Packet.EOP_SIZE]
		eop = data[-1 * Packet.EOP_SIZE:]

		# verifica se o EOP é valido
		if eop != Packet.EOP_LIST: raise Protocol.PayloadError('Tamanho de payload errado')
