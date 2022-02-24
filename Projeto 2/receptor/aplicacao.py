'''

Camada Física da Computação, 2022.1
Script de recepção de comandos do Projeto 2

Gabriel Onishi
Jerônimo Afrange

'''

serialName = "/dev/cu.usbmodem14201"  # Mac    (variacao de)
#serialName = "COM3"                  # Windows(variacao de)


def main():

    try:
        
        # #declaramos um objeto do tipo enlace com o nome "com" e ativa comunicação
        com1 = enlace(serialName)
        com1.enable()
        
        # dados a serem transmitidos (bytes da imagem "imagem.png")
        local_imagem = "./imagem.png"
        txBuffer = open(local_imagem, 'rb').read()    

        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
        tamanho_imagem = len(txBuffer)
            
        # verbose de início de transmissão
        print("*"*50)
        print("Início da transmissão")
        print("Enviando " + local_imagem + " (%d bytes)" % tamanho_imagem)

        # início da transmissão
        start = time.time()                     # momento do início da transmissão
        com1.sendData(np.asarray(txBuffer))     # envio dos dados
        end = time.time()                       # momento ao final da transmissão
        delta = end - start                     # tempo de transmissão

        # verbose do tempo de recepção
        delta_ms_aprox = round(delta * 1000, 3)
        print("Tempo de envio: ~" + str(delta_ms_aprox) + " ms")
       
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        txSize = com1.tx.getStatus()
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen

        arquivo_imagem_recebida = "./imagemrecebida.png"

        # verbose de recepção de dados
        print("*"*50)
        print("Recebendo dados...")
      
        # acesso aos bytes recebidos
        txLen = len(txBuffer)         
        start = time.time()                 # momento do início da leitura
        rxBuffer, nRx = com1.getData(txLen) # faz a leitura do buffer (bytes e tamanho)
        end = time.time()
        delta = end - start

        # verbose de recepção de dados
        delta_aprox = round(delta, 2)
        print("Tempo de recepção: ~" + str(delta_aprox) + "s (%d bytes)" % nRx)
        print("Salvando imagem em " + arquivo_imagem_recebida)

        print("*"*50)

        f = open(arquivo_imagem_recebida, 'wb')
        f.write(rxBuffer)

        f.close()
    
        # Encerra comunicação
        print("\nComunicação encerrada")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()