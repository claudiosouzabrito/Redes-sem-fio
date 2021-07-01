
from enlaceIn import checagem


def indo(hostOrigin, pacote, hostAlvoId):
    pacote.indo = hostAlvoId
    hostOrigin.ready2send = 0



def vindo(pacote, hostChegada, host, statusNewInsert):
    hostChegada.entryBox.append(pacote)
    if(pacote.indo == pacote.destino):
        pacote.status = 0 
    pacote.indo = -1

    checagem(pacote, hostChegada, host, statusNewInsert)
