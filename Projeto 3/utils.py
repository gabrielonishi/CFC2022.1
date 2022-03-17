"""
    Arquivo de utilidades
"""

def splitBytes(data):
    split_data = [data[i:i + 1] for i in range(0, len(data), 1)]
    result = list()
    for data in split_data:
        result.append(bytes(data))
    return result



def tryAgainPrompt():

    while True:

        answer = input("Tentar novamente? S/N\n")
        if answer.upper() == "N": return False
        elif answer.upper() == "S": return True
        else: print("Não entendi.\n")
