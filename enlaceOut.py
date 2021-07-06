import logging
from pacote import Pacote
from fisica import indo


def dados(hostOrigin, pacote, idDestino):   #função para enviar qualquer coisa que não seja ack
    logging.info("(ENLACE)\t\t\t\t\tPrepara para enviar pacote: "+str(pacote.message)+" para host "+str(pacote.destino))
    indo(pacote, idDestino)
    hostOrigin.ackWait = 3            #poe o host em espera por ack
    logging.info("(ENLACE)\t\t\t\t\tEntra em modo de espera ack")
    
    hostOrigin.statusEnlace = 1
    hostOrigin.block = 1               # Coloca a rede em bloqueio para evitar colisão
    logging.info("(ENLACE)\t\t\t\t\tBloqueia o canal para seus vizinhos")
    hostOrigin.pckAlvo = idDestino

def ack(hostOrigin):    #função para enviar ack, também bloqueia a rede
    ack = Pacote(-1, hostOrigin.id, hostOrigin.ackAlvo, "ACK")
    logging.info("(ENLACE)\t\t\t\t\tPrepara para enviar pacote ack")
    indo(ack, hostOrigin.ackAlvo)
    hostOrigin.statusEnlace = 0  
    hostOrigin.block = 1
    logging.info("(ENLACE)\t\t\t\t\tBloqueia o canal para seus vizinhos")
    return ack

