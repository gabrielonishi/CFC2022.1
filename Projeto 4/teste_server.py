from protocol import Protocol
from enlace import Enlace
import time

SERIAL_PORT_NAME = "/dev/cu.usbmodem14201"


# criação das instâncias de Enlace e Protocol
com1 = Enlace(SERIAL_PORT_NAME)
com1.enable()
time.sleep(0.2)
protocol = Protocol(com1)

# byte de sacrifício
print("Esperando 1 byte de sacrifício...")
rxBuffer, nRx = com1.getData(1, time_limit=1e12)
com1.rx.clearBuffer()
print("OK\n")
time.sleep(.2)

# teste do Protocol.getHead
print('Aguardando pacote de teste...')
head = protocol.getHead(time_limit=600)
print("OK\n")
print(head)

