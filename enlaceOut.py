from pacote import Pacote
from fisica import indo

def rts(hostOrigin, hostsDestino, id, host, ctsNewInsert):
    

    if(hostsDestino.id == id):
        rts = Pacote(-1, hostOrigin.id, hostsDestino.id, "RTS-1")
        #host[id].ctsAlvo.insert(0, hostOrigin.id)
        ctsNewInsert.append(tuple([id, hostOrigin.id]))
        #print("host "+str(id)+ " entrando")
        indo(hostOrigin, rts, hostsDestino.id)
    else:
        rts = Pacote(-1, hostOrigin.id, hostsDestino.id, "RTS-0")
        indo(hostOrigin, rts, hostsDestino.id)
    return rts

def cts(hostOrigin, hostsDestino, host, rtsNewInsert):
    hostOrigin.statusEnlace[0] = -1

    if(hostsDestino.id == hostOrigin.ctsAlvo[0]):
        cts = Pacote(-1, hostOrigin.id, hostsDestino.id, "CTS-1")
        #host[hostsDestino.id].rtsAlvo.insert(0, hostOrigin.id) 
        rtsNewInsert.append(tuple([hostsDestino.id, hostOrigin.id]))
        indo(hostOrigin, cts, hostsDestino.id)
    else:
        cts = Pacote(-1, hostOrigin.id, hostsDestino.id, "CTS-0")
        indo(hostOrigin, cts, hostsDestino.id)
    return cts

def dados(hostOrigin, hostDestino, pacote):
    indo(hostOrigin, pacote, hostDestino)
    hostOrigin.statusEnlace[0] = 0
    hostOrigin.freeze = 2
    hostOrigin.rtsAlvo.pop(0)

def ack(hostOrigin):
    hostOrigin.statusEnlace[0] = 0  #status conflitante???? sim

    ack = Pacote(-1, hostOrigin.id, hostOrigin.ctsAlvo[0], "ACK")
    indo(hostOrigin, ack, hostOrigin.ctsAlvo[0])
    hostOrigin.ctsAlvo.pop(0)
    
    return ack

    