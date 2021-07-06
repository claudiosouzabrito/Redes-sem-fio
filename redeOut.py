import logging
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
        # logging.info("\talcança " + str(origem.id)+" -> " + str(destino.id))
        return dist
    else:
        # logging.info("\tnão alcança")
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



def broadcast(REQ, origem, destino, pacotes):
    if(REQ):    #caso seja necessario enviar RREQ
        rota = str(origem.id)
        newId = uuid.uuid4()
        origem.rrepWait = 1

        aux = 0
    
        for idH in origem.vizinho: 
            aux += 1
            logging.info("(REDES)\t\t\t\tCriando rreq para host "+str(idH))
            rreq = Pacote(newId, origem.id, idH, "RREQ:"+str(origem.id)+"-"+str(destino)+":"+rota)  #cria RREQs para mandar para os vizinhos
            rreq.oldIds.append(origem.id)
            pacotes.append(rreq)
            origem.pacote.insert(0, rreq)

        if(aux > 0):
            dados(origem, origem.pacote[0], origem.pacote[0].destino) #enviando 1 RREQ por vez
        else:
            origem.incapacitado = 1
            for p in origem.pacote:
                p.status = 0
            logging.info("(REDES)\t\t\t\tNao tem vizinho nenhum para mandar o RREQ, host incapacitado de enviar mensagem ")

    else:  #caso não, enviar pacote via broadcast
        if(origem.pacote[0].message[:4] != 'RREQ' and origem.pacote[0].message[:4] != 'RREP'):
            pack2send = origem.pacote.pop(0)
            pack2send.status = 0
        
            
            for idH in origem.vizinho:
                if(idH not in pack2send.oldIds):  #se o host ainda não recebeu esse pacote antes
                    logging.info("(REDES)\t\t\t\tCriando copia do pacote "+str(pack2send.message)+" para "+str(idH))
                    pack2send2 = Pacote(pack2send.id, origem.id, idH, pack2send.message) #multiplicando os pacotes para enviar para cada vizinho
                    pack2send2.oldIds = copy.deepcopy(pack2send.oldIds)
                    pack2send2.oldIds.append(origem.id)
                    pack2send2.jaClonado = 1

                    pacotes.append(pack2send2)
                    origem.pacote.insert(0, pack2send2)

            #print(str(pack2send.destino) +" vs "+ str(pack2send2.destino))
        dados(origem, origem.pacote[0], origem.pacote[0].destino)
        
    

def redes(h, pacotes):

    if (randrange(10) > 1): #simulando falha de enlace
        request = False
    else:
        request = True
            
    if(h.statusEnlace == 0):  #estado de envio, ou resolvido

        if(h.rrepWait == 1):
            logging.info("(REDES)\t\t\tHost " +str(h.id)+ " esta esperando reply")
            for i in range(len(h.pacote)):
                if(h.pacote[i].message[:4] == 'RREQ' or h.pacote[i].message[:4] == 'RREP'):
                    pack2send = h.pacote[i]
                    logging.info("(REDES)\t\t\t\t mas repassou "+str(pack2send.message))
                    dados(h, pack2send, pack2send.destino)
                    break
        else:
            pack2send = h.pacote[0]
            #logging.info("\tdestino: "+str(pack2send.destino))
            if(pack2send.jaClonado == 1):
                logging.info("(REDES)\t\t\tHost " +str(h.id)+ " proximo pacote ja foi disparado na rede, nao precisa clonar de novo")
                dados(h, pack2send, pack2send.destino)
            else:
                if(pack2send.destino in h.vizinho):    #esse é igual
                    logging.info("(REDES)\t\t\tHost " +str(h.id)+ " planeja enviar pacote "+str(pack2send.message)+ " para seus vizinhos")
                    broadcast(False, h, pack2send.destino, pacotes)  
                else:
                    if(len(h.rotas[pack2send.destino]) > 0 and (not request)):   #a esse
                        logging.info("(REDES)\t\t\tHost " +str(h.id)+ " quer fazer chegar ate host "+str(pack2send.destino)+" mas nao eh vizinho")
                        broadcast(False, h, pack2send.destino, pacotes)  
                    elif(len(h.rotas[pack2send.destino]) > 0 and request):
                        logging.info("(REDES)\t\t\tHost " +str(h.id)+ " perdeu rota ate host "+str(pack2send.destino)+" por causa do erro de enlace, portanto, RREQ")
                        h.rotas[pack2send.destino] = []
                        broadcast(True, h, pack2send.destino, pacotes)  
                    else:
                        logging.info("(REDES)\t\t\tHost " +str(h.id)+ " nao tem rota, portanto, RREQ")
                        broadcast(True, h, pack2send.destino, pacotes)  
            
    elif(h.statusEnlace == 1):   #estado de espera por ack
        pack2send = h.pacote[0]
        #logging.info("\tdestino: "+str(pack2send.destino))

        if(h.ackWait == 0):     #espera acabou, mandando novamente
            logging.info("(REDES)\t\t\tHost " +str(h.id)+ " esperou ack e nao recebeu, planeja reenviar pacote para host "+str(pack2send.destino)+ ", pois eh vizinho")
            
            dados(h, pack2send, pack2send.destino) 
            
        else:
            logging.info("(REDES)\t\t\tHost " +str(h.id)+ " esperando ack")
            h.ackWait -= 1
            #print(str(h.id)+" com ackWait indo para "+str(h.ackWait))

    elif(h.statusEnlace == 2):  #estado de enviar ack
        logging.info("(REDES)\t\t\tHost " +str(h.id)+ " planeja enviar confirmacao de pacote ACK de volta para host "+str(h.ackAlvo))
        ACK = ack(h)
        pacotes.append(ACK)
    
    