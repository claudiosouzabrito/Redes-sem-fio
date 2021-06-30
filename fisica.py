
from enlaceIn import checagem


def indo(pacote, hostAlvoId):
    pacote.indo = hostAlvoId



def vindo(pacote, hostChegada, host):
    hostChegada.entryBox.append(pacote)
    if(pacote.indo == pacote.destino):
        pacote.status = 0 
    pacote.indo = -1

    checagem(pacote, hostChegada, host)
