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



def broadcast(REQ, origem, destino, pacotes, host):
    if(REQ):    #caso seja necessario enviar RREQ
        rota = str(origem.id)
        newId = uuid.uuid4()
        origem.rrepWait = 1
    
        for idH in origem.vizinho: 
            print("\t\t\tCriando rreq para "+str(idH))
            rreq = Pacote(newId, origem.id, idH, "RREQ:"+str(origem.id)+"-"+str(destino)+":"+rota)  #cria RREQs para mandar para os vizinhos
            rreq.oldIds.append(origem.id)
            pacotes.append(rreq)
            origem.pacote.insert(0, rreq)
 
        dados(origem, origem.pacote[0], origem.pacote[0].destino, host) #enviando 1 RREQ por vez

    else:  #caso não, enviar pacote via broadcast
        if(origem.pacote[0].message[:4] != 'RREQ' and origem.pacote[0].message[:4] != 'RREP'):
            pack2send = origem.pacote.pop(0)
            pack2send.status = 0
        
            
            for idH in origem.vizinho:
                if(idH not in pack2send.oldIds):  #se o host ainda não recebeu esse pacote antes
                    print("\t\t\tCriando copia do pacote "+str(pack2send.message)+" para "+str(idH))
                    pack2send2 = Pacote(pack2send.id, origem.id, idH, pack2send.message) #multiplicando os pacotes para enviar para cada vizinho
                    pack2send2.oldIds = copy.deepcopy(pack2send.oldIds)
                    pack2send2.oldIds.append(origem.id)
                    pack2send2.jaClonado = 1

                    pacotes.append(pack2send2)
                    origem.pacote.insert(0, pack2send2)

            #print(str(pack2send.destino) +" vs "+ str(pack2send2.destino))
        dados(origem, origem.pacote[0], origem.pacote[0].destino, host)
        
    

def redes(h, block, host, pacotes):

    if (randrange(10) > 1): #simulando falha de enlace
        request = False
    else:
        request = True
            
    if(h.statusEnlace == 0):  #estado de envio, ou resolvido

        if(h.rrepWait == 1):
            print("\t\tHost " +str(h.id)+ " esta esperando reply")
            for i in range(len(h.pacote)):
                if(h.pacote[i].message[:4] == 'RREQ' or h.pacote[i].message[:4] == 'RREP'):
                    pack2send = h.pacote[i]
                    print("\t\t\t mas repassou "+str(pack2send.message))
                    dados(h, pack2send, pack2send.destino, host)
                    break
        else:
            pack2send = h.pacote[0]
            #print("destino: "+str(pack2send.destino))
            if(pack2send.jaClonado == 1):
                print("\t\tHost " +str(h.id)+ " proximo pacote ja foi disparado na rede, nao precisa clonar de novo")
                dados(h, pack2send, pack2send.destino, host)
            else:
                if(pack2send.destino in h.vizinho):    #esse é igual
                    print("\t\tHost " +str(h.id)+ " envia pacote para seus vizinhos "+str(pack2send.message))
                    broadcast(False, h, pack2send.destino, pacotes, host)  
                else:
                    if(len(h.rotas[pack2send.destino]) > 0 and (not request)):   #a esse
                        print("\t\tHost " +str(h.id)+ " quer fazer chegar até "+str(pack2send.destino)+" mas nao eh vizinho")
                        broadcast(False, h, pack2send.destino, pacotes, host)  
                    elif(len(h.rotas[pack2send.destino]) > 0 and request):
                        print("\t\tHost " +str(h.id)+ " perdeu rota até "+str(pack2send.destino)+" por causa do erro de enlace, portanto, RREQ")
                        h.rotas[pack2send.destino] = []
                        broadcast(True, h, pack2send.destino, pacotes, host)  
                    else:
                        print("\t\tHost " +str(h.id)+ " não tem rota, portanto, RREQ")
                        broadcast(True, h, pack2send.destino, pacotes, host)  
            
    elif(h.statusEnlace == 1):   #estado de espera por ack
        pack2send = h.pacote[0]
        #print("destino: "+str(pack2send.destino))

        if(h.ackWait == 0):     #espera acabou, mandando novamente
            print("\t\tHost " +str(h.id)+ " esperou ack e nao recebeu, reenviando pacote para "+str(pack2send.destino)+ ", pois é vizinho")
            
            dados(h, pack2send, pack2send.destino, host) 
            
        else:
            print("\t\tHost " +str(h.id)+ " esperando ack")
            h.ackWait -= 1
            #print(str(h.id)+" com ackWait indo para "+str(h.ackWait))

    elif(h.statusEnlace == 2):  #estado de enviar ack
        print("\t\tHost " +str(h.id)+ " envia confirmacao de pacote ACK de volta para "+str(h.ackAlvo))
        ACK = ack(h)
        pacotes.append(ACK)
    
    