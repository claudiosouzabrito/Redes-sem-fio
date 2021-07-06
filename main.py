from redeOut import Distance_Matrix, redes
from graph import graph
from host import Host 
import json
from pacote import Pacote
from fisica import vindo
import logging

logging.basicConfig(filename='resultados/descricao.log', filemode='w', format='%(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)

logging.info("\tApresentando os hosts:")

fileH = open('entradas/hospedeiros.txt', 'r' ).readlines()
dimensions = fileH[0].split()
dimension = int(dimensions[1]) - int(dimensions[0])

numHost = int(fileH[1])
host = []
x = []
y = []
ranges = []
nomes = []

for i in range(2, len(fileH)):
    jay = json.loads(fileH[i])
    x.append(jay["x"])
    y.append(jay["y"])
    ranges.append(jay["range"])
    nomes.append('host' + str(i-2))

    hos = Host(i-2, jay["x"], jay["y"], jay["range"])
    logging.info('\t\tid: ' + str(hos.id) + ', x: ' + str(hos.x) + ', y: ' + str(hos.y) + ', range: ' + str(hos.range))
    host.append(hos)

logging.info("\tApresentando os pacotes:")

pacote = []

fileP = open('entradas/pacotes.txt', 'r').readlines()
for i in range(len(fileP)):
    jay = json.loads(fileP[i])
    pck = Pacote(i, jay["origin"], jay["destino"], jay["message"])
    pck.message = str(pck.origin)+ "-"+ str(pck.destino)+'/'+pck.message
    pck.oldIds.append(pck.origin)

    logging.info('\t\tid: ' +str(i)+ ', origin: ' + str(pck.origin) + ', destino: ' + str(pck.destino) + ', mensagem: ' + str(pck.message))
    pacote.append(pck)

    host[jay["origin"]].pacote.append(pck)
    host[jay["origin"]].oldIds.append(pck.id)

graph(x,y,ranges, nomes, numHost, dimension)

distances = Distance_Matrix(host)

for h in host:
    for i in range(len(host)):
        a = []
        h.rotas.append(a)
    for v in h.vizinho:
        h.rotas[v].append(h.id)
        h.rotas[v].append(v)



stillGoing = 1
round = 0
while stillGoing:
    ctrl1 = 0
    ctrl2 = 0
    block = 0

    logging.info("\n")
    logging.info("\tRound "+str(round))

    logging.info("\t\tRecebimentos:")
    for p in pacote:
        if(p.indo >= 0): #se no round anterior ele foi enviado por alguem
            if(host[p.indo].surdo):
                logging.info("\t\t\t\t\tPacote " +str(p.message)+ " enviado por "+str(p.origin)+" chegou no host " +str(p.indo)+ ", mas foi ignorado pois estava surdo (colisao)")
                p.indo = -1
            else:
                vindo(p, host[p.indo], host, pacote)   
    print()
    logging.info("\t\tFilas de pacotes nos hosts:")
    for h in host:
        
        if(len(h.pacote) == 0):
            logging.info("\t\t\tHost " +str(h.id)+ " nao tem pacote nenhum para mandar")
        else:
            logging.info("\t\t\tHost " +str(h.id)+ " possui os seguintes pacotes para enviar: ")
            for p in h.pacote:
                if(p.indo == -1):
                    logging.info("\t\t\t\t" + str(p.message))
                else:
                    logging.info("\t\t\t\t" + str(p.message)+" ja enviado")

    logging.info("\n")
    logging.info("\t\tMovimentos: ")
    for h in host:
        if(len(h.pacote) or h.statusEnlace == 2):
            
            for i in h.vizinho:     #PROCURAR NOS VIZINHOS SE TEM ALGUEM BLOQUEANDO
                block += host[i].block
            if(block):         #caso algum host ja esteja transmitindo
                if(h.statusEnlace == 0):
                    pack2send = h.pacote[0]
                    if(h.rrepWait == 1):
                        logging.info("\t\t\t\t\tHost " +str(h.id)+ " esta a espera de reply, canal bloqueado")
                    else:
                        logging.info("\t\t\t\t\tHost " +str(h.id)+ " quer enviar "+str(pack2send.message)+ " com destino a "+str(pack2send.destino)+ " mas canal bloqueado")
                elif(h.statusEnlace == 1):
                    pack2send = h.pacote[0]
                    if(h.ackWait == 0):
                        logging.info("\t\t\t\t\tHost " +str(h.id)+ " esperou o ack, mas nao recebeu nada, quer reenviar pacote "+str(pack2send.message)+ " com destino a "+str(pack2send.destino)+ " mas canal bloqueado")
                    else:
                        h.ackWait -= 1
                        logging.info("\t\t\t\t\tHost " +str(h.id)+ " esta esperando ack, canal bloqueado")
                elif(h.statusEnlace == 2):
                    logging.info("\t\t\t\t\tHost " +str(h.id)+ " quer enviar ack com destino a "+str(h.ackAlvo)+ " mas canal bloqueado")
                

            else:
                # if(len(host[1].pacote) > 0):
                #     print(host[1].pacote[0].destino)
                redes(h, pacote)  #enviar na rede
            


        else:
            logging.info("\t\t\t\t\tHost " +str(h.id)+ " nao tem nada para enviar")


        aux = 0
        for p in h.entryBox:
            if(p.status == 0):
                #logging.info("\t\t\t\tpacote " + str(p.message)+ " entrado em " +str(h.id)+ " chegou ao destino final correto ")
                h.entryBox.pop(aux)  #pacote resolvido
            # else:
                # logging.info("\t\t\t\tpacote " + str(p.message)+ " entrado em " +str(h.id)+ " tem outro destino: "+str(p.destino))
                # pack = h.entryBox.pop(aux)
                # pack.origin = h.id
                # h.pacote.append(pack)  #pacote enviado para a lista de pacotes do host
            aux += 1
    
    for p in pacote:
        ctrl1 += p.status
        if(ctrl1 > 0):
            break
    for h in host:
        h.block = 0
        h.surdo = False
        #logging.info("\t\tHost "+str(h.id)+ " está em status = "+str(h.statusEnlace))
        if(h.statusEnlace > 0):
            ctrl2 = 1

    if(ctrl1 or ctrl2):
        stillGoing = 1
    else:
        stillGoing = 0
    
    round += 1
    
    