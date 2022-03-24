
from packet import Packet
import utils

class Protocol:
	'''
	Representa o protocolo de comunicação a ser implementado
	no projeto 4.

	'''


	def __init__(self, enlace):
		''' Cria uma nova instância de Protocol '''
		
		# amarra o enlace ao protocolo
		self.enlace = enlace
	

	def getHead(self):
		''' Chama getData para o tamanho do head e retorna os dados obtidos em lista de byte '''

		data = self.enlace.getData(Packet.HEAD_SIZE)
		bytes_list = 
		return 

