from enlaceIn import checagem

def indo(pacote, hostAlvoId):  #função base para enviar qualquer pacote para qualquer host, apenas atualiza o estado do pacote
    pacote.indo = hostAlvoId



def vindo(pacote, hostChegada, host, pacotes):  #função para receber pacotes. Após a checagem decide se o pacote será ignorado ou não


    ok = checagem(pacote, hostChegada, host, pacotes)

    if(ok):
        hostChegada.entryBox.append(pacote)
        
        if(pacote.indo == pacote.destino):
            pacote.status = 0 
    
    pacote.indo = -1

    
