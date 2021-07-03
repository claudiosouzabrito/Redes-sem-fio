def checagem(pacote, hostChegada, host):
    if(pacote.message == 'ACK'):
        hostChegada.ackWait = 0
        hostChegada.statusEnlace = 0
        hostChegada.pacote.pop(0)
        host[pacote.origin].ackAlvo.pop(0)
        return True
    else:
        if(hostChegada.statusEnlace != 1 or (hostChegada.statusEnlace == 1 and pacote.origin == hostChegada.pckAlvo)): 
            hostChegada.statusEnlace = 2 # vai mandar o ACK
            hostChegada.surdo = True
            return True
        else:
            return False




    