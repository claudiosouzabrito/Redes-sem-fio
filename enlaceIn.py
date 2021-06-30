def checagem(pacote, hostChegada, host):
    if(pacote.message == 'RTS-1'):
        hostChegada.statusEnlace.insert(0,1) # vai mandar cts
        hostChegada.freeze = -1

    elif(pacote.message == 'RTS-0'):
        if(host[pacote.origin].freeze == 0):
            host[pacote.origin].freeze = -1
        if(hostChegada.freeze != -1):
            hostChegada.freeze = 2     

    elif(pacote.message == 'CTS-1'): 
        hostChegada.statusEnlace[0] = 2  # vai mandar a mensagem
        hostChegada.freeze = -1

    elif(pacote.message == 'CTS-0'):
        if(host[pacote.origin].freeze == 0):
            host[pacote.origin].freeze = -1
        if(hostChegada.freeze != -1):
            hostChegada.freeze = 2 

    elif(pacote.message == 'ACK'):
        hostChegada.statusEnlace.pop(0) # começou ou finalizou
    else:
        hostChegada.statusEnlace[0] = 3 # vai mandar o ACK



    