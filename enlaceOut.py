from pacote import Pacote
from fisica import indo

def rts(hostOrigin, hostsDestino, id, host):
    hostOrigin.statusEnlace = -1

    if(hostsDestino.id == id):
        rts = Pacote(-1, hostOrigin.id, hostsDestino.id, "RTS-1")
        host[id].ctsAlvo = hostOrigin.id
        indo(rts, hostsDestino.id)
    else:
        rts = Pacote(-1, hostOrigin.id, hostsDestino.id, "RTS-0")
        indo(rts, hostsDestino.id)
    return rts

def cts(hostOrigin, hostsDestino, host):
    hostOrigin.statusEnlace = -1

    if(hostsDestino.id == hostOrigin.ctsAlvo):
        cts = Pacote(-1, hostOrigin.id, hostsDestino.id, "CTS-1")
        host[hostsDestino.id].rtsAlvo = hostOrigin.id
        indo(cts, hostsDestino.id)
    else:
        cts = Pacote(-1, hostOrigin.id, hostsDestino.id, "CTS-0")
        indo(cts, hostsDestino.id)
    return cts

def dados(hostOrigin, hostDestino, pacote):
    indo(pacote, hostDestino)
    hostOrigin.statusEnlace = 0

def ack(hostOrigin):
    hostOrigin.statusEnlace = 0

    ack = Pacote(-1, hostOrigin.id, hostOrigin.ctsAlvo, "ACK")
    indo(ack, hostOrigin.ctsAlvo)
    
    return ack

    