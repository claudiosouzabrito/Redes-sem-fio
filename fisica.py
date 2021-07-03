from enlaceIn import checagem

def indo(pacote, hostAlvoId):
    pacote.indo = hostAlvoId



def vindo(pacote, hostChegada, host):

    ok = checagem(pacote, hostChegada, host)
    if(ok):
        hostChegada.entryBox.append(pacote)
        if(pacote.indo == pacote.destino):
            pacote.status = 0 
    pacote.indo = -1

    
