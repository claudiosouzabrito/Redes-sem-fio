from pacote import Pacote
from fisica import indo


def dados(hostOrigin, pacote, idDestino, host):
    indo(pacote, idDestino)
    hostOrigin.ackWait = 2
    host[idDestino].ackAlvo.append(hostOrigin.id)
    hostOrigin.statusEnlace = 1
    hostOrigin.block = 1
    hostOrigin.pckAlvo = idDestino

def ack(hostOrigin):
    ack = Pacote(-1, hostOrigin.id, hostOrigin.ackAlvo[0], "ACK")
    indo(ack, hostOrigin.ackAlvo[0])
    hostOrigin.statusEnlace = 0  

    return ack

def enlace(h, block, host, pacote):
    if(h.statusEnlace == 0):
        pack2send = h.pacote[0]

        if(block == 0):
            #USAR ALGORITMO DE REDES PRA ACHAR O ALVO PRO TERCEIRO PARÂMETRO
            dados(h, h.pacote[0], h.pacote[0].destino, host)
            print("\t\tHost " +str(h.id)+ " envia pacote "+str(pack2send.message)+ " com destino a "+str(pack2send.destino))
        else:
            print("\t\tHost " +str(h.id)+ " quer enviar "+str(pack2send.message)+ " com destino a "+str(pack2send.destino)+ " mas canal bloqueado")
        
    elif(h.statusEnlace == 1):
        if(h.ackWait == 0):
            pack2send = h.pacote[0]
            if(block ==0):
                #USAR ALGORITMO DE REDES PRA ACHAR O ALVO PRO TERCEIRO PARÂMETRO
                dados(h, h.pacote[0], h.pacote[0].destino, host)
                print("\t\tHost " +str(h.id)+ " esperou o ack, mas nao recebeu nada, reenviando pacote "+str(pack2send.message)+ " com destino a "+str(pack2send.destino))
            else:
                print("\t\tHost " +str(h.id)+ " esperou o ack, mas nao recebeu nada, quer reenviar pacote "+str(pack2send.message)+ " com destino a "+str(pack2send.destino)+ " mas canal bloqueado")

        else:
            print("\t\tHost " +str(h.id)+ " esperando ack")
            h.ackWait -= 1

    elif(h.statusEnlace == 2):
        print("\t\tHost " +str(h.id)+ " envia confirmacao de pacote ACK de volta para "+str(h.ackAlvo[0]))
        ACK = ack(h)
        pacote.append(ACK)