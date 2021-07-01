import copy
from enlaceOut import ack, cts, dados, rts
from graph import graph
from host import Host 
import json
from pacote import Pacote
from fisica import vindo

print("Apresentando os hosts:")

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
    print('\tid: ' + str(hos.id) + ', x: ' + str(hos.x) + ', y: ' + str(hos.y) + ', range: ' + str(hos.range))
    host.append(hos)

print("Apresentando os pacotes:")

pacote = []

fileP = open('entradas/pacotes.txt', 'r').readlines()
for i in range(len(fileP)):
    jay = json.loads(fileP[i])
    pck = Pacote(i, jay["origin"], jay["destino"], jay["message"])
    print('\tid: ' +str(i)+ ', origin: ' + str(pck.origin) + ', destino: ' + str(pck.destino) + ', mensagem: ' + str(pck.message))
    pacote.append(pck)

    host[jay["origin"]].pacote.append(pck)

graph(x,y,ranges, nomes, numHost, dimension)
stillGoing = 1
round = 0

while stillGoing:
    ctrl1 = 0
    ctrl2 = 0
    statusNewInserts = []
    rtsNewInserts = []
    ctsNewInserts = []

    print("\nRound "+str(round))

    print("\tStatus:")
    for p in pacote:
        if(p.indo >= 0): #se no round anterior ele foi enviado por alguem
            print("\t\tPacote " +str(p.message)+ " chegou no host " +str(p.indo))
            vindo(p, host[p.indo], host, statusNewInserts)   

    for h in host:
        if(len(h.pacote) == 0):
            print("\t\tHost " +str(h.id)+ " não tem pacote nenhum para mandar")
        else:
            print("\t\tHost " +str(h.id)+ " possui os seguintes pacotes para enviar: ")
            for p in h.pacote:
                print("\t\t\t" + str(p.message))

    print("\tMovimentos: ")
    for h in host:
        if(len(h.pacote) or h.statusEnlace[0] >= 1):
            if(h.ctsAlvo[0] > -1 and host[h.ctsAlvo[0]].freeze > 0 and h.statusEnlace[0] != 3):
                h.freeze = 2
            if(h.freeze <= 0):
                if(h.ready2send):
                    if(h.statusEnlace[0] == 0):
                        print("\t\tHost " +str(h.id)+ " envia RTS")
                        pack2send = h.pacote[0]
                        h.statusEnlace.insert(0,-1)
                        #statusNewInserts.append(tuple([h.id, -1]))

                        lista = copy.deepcopy(host)
                        lista.pop(h.id)
                        for h2 in lista:
                            RTS= rts(h, h2, pack2send.destino, host, ctsNewInserts) #REDES ENTRA AQUI
                            pacote.append(RTS) 
                            
                    elif(h.statusEnlace[0] == 1):
                        print("\t\tHost " +str(h.id)+ " envia CTS para confirmar reserva de canal")

                        lista = copy.deepcopy(host)
                        lista.pop(h.id)
                        for h2 in lista:
                            CTS = cts(h, h2, host, rtsNewInserts) #REDES ENTRA AQUI
                            pacote.append(CTS)

                    elif(h.statusEnlace[0] == 2):
                        dados(h, h.rtsAlvo[0], h.pacote[0])
                        pack2send = h.pacote.pop(0)
                        print("\t\tHost " +str(h.id)+ " envia pacote "+str(pack2send.id)+ " com destino a "+str(pack2send.destino))

                    elif(h.statusEnlace[0] == 3):
                        print("\t\tHost " +str(h.id)+ " envia confirmacao de pacote ACK de volta para "+str(h.ctsAlvo[0]))
                        #host[h.ctsAlvo[0]].statusEnlace[0] = 0  #liberando o alvo do CTS
                        ACK = ack(h)
                        pacote.append(ACK)
                        h.statusEnlace.pop(0)

                    else:
                        print("\t\tHost " +str(h.id)+ " em standby")
                else:
                    print("\t\tHost " +str(h.id)+ " quer enviar pacote")
                    #ALGORITMO DE PROCURA DE VIZINHANÇA AQUI (REDES)
                    h.ready2send = 1  #TEM Q ZERAR EM ALGUM MOMENTO
            else:
                print("\t\tHost" +str(h.id)+ " esta congelado")
                h.freeze -= 1
                
        else:
            print("\t\tHost " +str(h.id)+ " nao tem nada para enviar")

        aux = 0
        for p in h.entryBox:
            if(p.destino == h.id):
                print("\t\tpacote " + str(p.message)+ " entrado em " +str(h.id)+ " chegou ao destino final correto ")
                h.entryBox.pop(aux)
            else:
                print("\t\tpacote " + str(p.message)+ " entrado em " +str(h.id)+ " tem outro destino ")
                pack = h.entryBox.pop(aux)
                pack.origin = h.id
                h.pacote.append(pack)
            aux += 1

    for t in statusNewInserts:
        host[t[0]].statusEnlace.insert(0, t[1])
    for t in rtsNewInserts:
        host[t[0]].rtsAlvo.insert(0, t[1])
    for t in ctsNewInserts:
        host[t[0]].ctsAlvo.insert(0, t[1])
    
    for p in pacote:
        ctrl1 += p.status
        if(ctrl1 > 0):
            break
    for h in host:
        if(len(h.statusEnlace) > 1):
            ctrl2 = 1
            break
    if(ctrl1 or ctrl2):
        stillGoing = 1
    else:
        stillGoing = 0
    
    round += 1
    
    if(round == 17):
        break