"""
    Arquivo de utilidades
"""

def split_bytes(data): 
    return [data[i:i + 1] for i in range(0, len(data), 1)]



def tryAgainPrompt():

    while True:

        answer = input("Tentar novamente? S/N")
        if answer.upper() == "N": return False
        elif answer.upper() == "S": return True
        else: print("Não entendi.\n")
