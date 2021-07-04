from pacote import Pacote
from fisica import indo


def dados(hostOrigin, pacote, idDestino, host):   #função apra enviar qualquer coisa que não seja ack. Coloca a rede em bloqueio para evitar colisão, e ponhe o host em espera por ack
    indo(pacote, idDestino)
    hostOrigin.ackWait = 2
    host[idDestino].ackAlvo = hostOrigin.id
    hostOrigin.statusEnlace = 1
    hostOrigin.block = 1
    hostOrigin.pckAlvo = idDestino

def ack(hostOrigin):    #função para enviar ack, também bloqueia a rede
    ack = Pacote(-1, hostOrigin.id, hostOrigin.ackAlvo, "ACK")
    indo(ack, hostOrigin.ackAlvo)
    hostOrigin.statusEnlace = 0  
    hostOrigin.block = 1

    return ack

