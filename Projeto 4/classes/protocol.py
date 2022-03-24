
from packet import Packet
import utils

class Protocol:
	'''
	Representa o protocolo de comunicação a ser implementado
	no projeto 4.

	'''

	class ProtocolError(Exception):
		''' Erro genérico de protocolo '''
		pass

	class TimeoutError(ProtocolError):
		''' Erro de timeout '''
		pass

	class HeadError(ProtocolError):
		''' Erro de head inválido '''
		pass


	def __init__(self, enlace):
		''' Cria uma nova instância de Protocol '''
		
		# amarra o enlace ao protocolo
		self.enlace = enlace
	

	def getHead(self):
		''' Chama getData para o tamanho do head e retorna os dados obtidos em lista de byte '''

		# chama getData, gera um erro de Timeout caso dê timeout
		data = self.enlace.getData(Packet.HEAD_SIZE)
		if data is None: raise Protocol.TimeoutError()

		# converte os dados recebidos a uma lista de bytes
		bytes_list = utils.splitBytes(data)

		# extrai o tipo da mensagem do head e extrai o template relevante
		message_type = int.from_bytes(bytes_list[0])
		head_template = Packet.HEAD_TEMPLATES[message_type]

		# verifica a validade byte a byte
		for index in range(Packet.HEAD_SIZE):

			# extrai o byte esperado e o recebido das listas
			expected = head_template[index]
			received = bytes_list[index]

			# se o valor esperado for uma string, finalizar iteração
			if isinstance(expected, str): continue

			# verifica se o valor é o esperado
			if expected != received: raise Protocol.HeadError('Byte %d do HEAD inválido' % index)

		return bytes_list

	
	def getPayload(self, head):
		''' Chama getData para o tamanho do payload especificado em um head '''

		message_type = head[0]

		data = self.enlace.getData()

