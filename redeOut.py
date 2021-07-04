from random import randrange
from pacote import Pacote
from enlaceOut import ack, dados
import numpy as np
import copy
import uuid


def Distance(origem, destino):
    a = np.array((origem.x, origem.y))
    b = np.array((destino.x, destino.y))

    dist = np.linalg.norm(a-b)
    # print(dist)

    if(dist <= (origem.range)):
        # print("alcança " + str(origem.id)+" -> " + str(destino.id))
        return dist
    else:
        # print("não alcança")
        return float('inf')



def Distance_Matrix(host):
    distances = {}

    for i in range(len(host)):
        distances[i] = {}

    for i in range(len(host)):
        for j in range(len(host)):
            distances[i][j] = Distance(host[i], host[j])
            if(distances[i][j] != 0.0 and distances[i][j] != float('inf')):  #criando a matriz de distancias
                host[i].vizinho.append(j)

    for i in range(len(host)):
        print(str(i)+ ": " + str(distances[i]))


    return distances



def broadcast(request, origem, destino, pacotes, host):
    if(request):    #caso seja necessario enviar RREQ
        rota = str(origem.id)
        newId = uuid.uuid4()

        for idH in origem.vizinho: 
            print("\t\t\tCriando rreq para "+str(idH))
            rreq = Pacote(newId, origem.id, idH, "RREQ:"+str(origem.id)+"-"+str(destino)+":"+rota)  #cria RREQs para mandar para os vizinhos
            rreq.oldIds.append(origem.id)
            pacotes.append(rreq)
            origem.pacote.insert(0, rreq)
 
        dados(origem, origem.pacote[0], origem.pacote[0].destino, host) #enviando 1 RREQ por vez
        print("\t\t\tEnviando RREQ para "+str(origem.pacote[0].destino))

    else:  #caso não, enviar pacote via broadcast
        if(origem.pacote[0].destino in origem.vizinho):
            dados(origem, origem.pacote[0], origem.pacote[0].destino, host)
            print("\t\t\tEnviando pacote: "+str(origem.pacote[0].message)+" para "+str(origem.pacote[0].destino))

        else:
            pack2send = origem.pacote.pop(0)
            pack2send.status = 0

            
            for idH in origem.vizinho:
                if(idH not in pack2send.oldIds):  #se o host ainda não recebeu esse pacote antes
                    print("\t\t\tCriando copias dos pacotes para "+str(idH))
                    pack2send2 = Pacote(pack2send.id, origem.id, pack2send.destino, pack2send.message) #multiplicando os pacotes para enviar para cada vizinho
                    pack2send2.oldIds = copy.deepcopy(pack2send.oldIds)
                    pack2send2.oldIds.append(origem.id)

                    pacotes.append(pack2send2)
                    origem.pacote.insert(0, pack2send2)

            dados(origem, origem.pacote[0], origem.pacote[0].destino, host)
            print("\t\t\tEnviando pacote: "+str(origem.pacote[0].message)+" para "+str(origem.pacote[0].destino))

    

def redes(h, block, host, pacotes):

    if (randrange(10) > 1): #simulando falha de enlace
        request = False
    else:
        request = True
            
    if(h.statusEnlace == 0):  #estado de envio, ou resolvido
        pack2send = h.pacote[0]
        if(request):
            print("\t\tHost " +str(h.id)+ " falha de enlace, redescobrindo as rotas")
            if(pack2send.destino not in h.vizinho):
                print("\t\t\tnao tem rota para "+str(pack2send.destino)+ ", RREQ para vizinhos ")
                h.rotas[pack2send.destino] = []
                broadcast(True, h, pack2send.destino, pacotes, host)
            else:
                print("\t\t\tHost " +str(h.id)+ " tem rota para "+str(pack2send.destino)+ ", pois é vizinho")
                broadcast(False, h, pack2send.destino, pacotes, host)
        else:
            print("\t\tHost " +str(h.id)+ " pretende enviar pacote "+str(pack2send.message)+ " com destino a "+str(pack2send.destino))
            broadcast(False, h, pack2send.destino, pacotes, host)
            
    elif(h.statusEnlace == 1):   #estado de espera por ack
        pack2send = h.pacote[0]
        if(h.ackWait == 0):     #espera acabou, mandando novamente
            if(request):
                print("\t\tHost " +str(h.id)+ " falha de enlace, redescobrindo as rotas")
                if(pack2send.destino not in h.vizinho):
                    print("\t\t\tHost " +str(h.id)+ " nao tem rota para "+str(pack2send.destino)+ ", RREQ para vizinhos ")
                    h.rotas[pack2send.destino] = []
                    broadcast(True, h, pack2send.destino, pacotes, host)
                else:
                    print("\t\t\tHost " +str(h.id)+ " tem rota para "+str(pack2send.destino)+ ", pois é vizinho")
                    broadcast(False, h, pack2send.destino, pacotes, host)
            else:
                print("\t\tHost " +str(h.id)+ " esperou o ack, mas nao recebeu nada, pretendendo reenviar pacote "+str(pack2send.message)+ " com destino a "+str(pack2send.destino))
                broadcast(False, h, pack2send.destino, pacotes, host)
            
        else:
            print("\t\tHost " +str(h.id)+ " esperando ack")
            h.ackWait -= 1

    elif(h.statusEnlace == 2):  #estado de enviar ack
        print("\t\tHost " +str(h.id)+ " envia confirmacao de pacote ACK de volta para "+str(h.ackAlvo))
        ACK = ack(h)
        pacotes.append(ACK)
    