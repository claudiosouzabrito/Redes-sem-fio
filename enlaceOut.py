from pacote import Pacote
from fisica import indo


def dados(hostOrigin, pacote, idDestino, host):   #função apra enviar qualquer coisa que não seja ack
    print("\t\t\tHost "+str(hostOrigin.id)+" envia pacote: "+str(pacote.message)+" para "+str(pacote.destino))
    indo(pacote, idDestino)
    hostOrigin.ackWait = 2            #ponhe o host em espera por ack
    #print(str(hostOrigin.id)+" com ackWait indo para 2")
    #host[idDestino].ackAlvo = hostOrigin.id
    hostOrigin.statusEnlace = 1
    hostOrigin.block = 1               # Coloca a rede em bloqueio para evitar colisão
    hostOrigin.pckAlvo = idDestino

def ack(hostOrigin):    #função para enviar ack, também bloqueia a rede
    ack = Pacote(-1, hostOrigin.id, hostOrigin.ackAlvo, "ACK")
    indo(ack, hostOrigin.ackAlvo)
    hostOrigin.statusEnlace = 0  
    hostOrigin.block = 1

    return ack

