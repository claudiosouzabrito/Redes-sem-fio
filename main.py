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

stillGoing = 1
round = 0
graph(x,y,ranges, nomes, numHost, dimension, round)
while stillGoing:

    print("\nRound "+str(round))

    print("\tStatus:")
    for p in pacote:
        if(p.indo >= 0): #se no round anterior ele foi enviado por alguem
            print("\t\tPacote " +str(p.id)+ " chegou no host " +str(p.indo))
            vindo(p, host[p.indo])   

    for h in host:
        if(len(h.pacote) == 0):
            print("\t\tHost " +str(h.id)+ " não tem pacote nenhum para mandar")
        else:
            for p in h.pacote:
                print("\t\tHost " +str(h.id)+ " possui os seguintes pacotes para enviar: ")
                print("\t\t\t" + str(p.message))

    print("\tMovimentos: ")
    for h in host:
        if(len(h.pacote) or h.statusEnlace >= 1):
            if(h.ready2send):
                if(h.freeze == 0):
                    if(h.statusEnlace == 0):
                        print("\t\tHost " +str(h.id)+ " envia RTS")
                        pack2send = h.pacote[0]

                        lista = copy.deepcopy(host)
                        lista.pop(1)
                        for h2 in lista:
                            RTS= rts(h, h2, pack2send.destino, host) #REDES ENTRA AQUI
                            pacote.append(RTS) 
                            
                    elif(h.statusEnlace == 1):
                        print("\t\tHost " +str(h.id)+ " envia CTS para confirmar reserva de canal")

                        lista = copy.deepcopy(host)
                        lista.pop(2)
                        for h2 in lista:
                            CTS = cts(h, h2, host) #REDES ENTRA AQUI
                            pacote.append(CTS)

                    elif(h.statusEnlace == 2):
                        dados(h, h.rtsAlvo, h.pacote[0])
                        pack2send = h.pacote.pop(0)
                        print("\t\tHost " +str(h.id)+ " envia pacote "+str(pack2send.id)+ " com destino a "+str(pack2send.destino))

                    elif(h.statusEnlace == 3):
                        print("\t\tHost " +str(h.id)+ " envia confirmacao de pacote ACK de volta para "+str(h.ctsAlvo))
                        ack = ack(h)
                        pacote.append(ack)

                    else:
                        print("\t\tHost " +str(h.id)+ " em standby")
                else:
                    print("\t\tHost" +str(h.id)+ " esta congelado")
                    h.freeze -= 1
            else:
                print("\t\tHost " +str(h.id)+ " quer enviar pacote")
                #ALGORITMO DE PROCURA DE VIZINHANÇA AQUI
                h.ready2send = 1
        else:
            print("\t\tHost " +str(h.id)+ " nao tem nada para enviar")

        if(len(h.entryBox)):
            if(h.entryBox[0].destino == h.id):
                print("\t\tpacote entrado em " +str(h.id)+ " foi o correto ")
                h.entryBox.pop(0)
            else:
                print("\t\tpacote entrado em " +str(h.id)+ " tem outro destino ")
                h.pacote.append(h.entryBox.pop(0))
    
    stillGoing = 0
    for p in pacote:
        print(p.message)
        stillGoing += p.status
        if(stillGoing > 0):
            break
    
    round += 1

