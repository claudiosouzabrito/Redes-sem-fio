def checagem(pacote, hostChegada):
    if(pacote.message == 'RTS-1'):
        hostChegada.statusEnlace = 1
    elif(pacote.message == 'RTS-0'):
        hostChegada.freeze = 2
    elif(pacote.message == 'CTS-1'):
        hostChegada.statusEnlace = 2
    elif(pacote.message == 'CTS-0'):
        hostChegada.freeze = 2
    elif(pacote.message == 'ACK'):
        hostChegada.statusEnlace = 0
    else:
        hostChegada.statusEnlace = 3