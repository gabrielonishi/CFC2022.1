"""
    Arquivo de utilidades
"""
def split_bytes(data): 
    return [data[i:i + 1] for i in range(0, len(data), 1)]
