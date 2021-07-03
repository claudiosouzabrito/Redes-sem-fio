import copy
from enlaceOut import enlace
from graph import graph
from host import Host 
import json
from pacote import Pacote
from fisica import vindo
from random import randrange

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
    block = 0

    print("\nRound "+str(round))

    print("\tStatus:")
    for p in pacote:
        if(p.indo >= 0): #se no round anterior ele foi enviado por alguem
            if(host[p.indo].surdo):
                print("\t\tPacote " +str(p.message)+ " enviado por "+str(p.origin)+" chegou no host " +str(p.indo)+ ", mas foi ignorado pois estava surdo")
            else:
                print("\t\tPacote " +str(p.message)+ " enviado por "+str(p.origin)+" chegou no host " +str(p.indo))
                vindo(p, host[p.indo], host)   
    print()
    for h in host:
        print("\tHost "+str(h.id)+ " está em status = "+str(h.statusEnlace))
        if(len(h.pacote) == 0):
            print("\t\tHost " +str(h.id)+ " não tem pacote nenhum para mandar")
        else:
            print("\t\tHost " +str(h.id)+ " possui os seguintes pacotes para enviar: ")
            for p in h.pacote:
                print("\t\t\t" + str(p.message))

    print("\tMovimentos: ")
    for h in host:
        if(len(h.pacote) or h.statusEnlace == 2):
            if(randrange(10) >= 2): #simulando falha de enlace
                copia = copy.deepcopy(host)
                copia.pop(h.id)
                for h2 in copia:     #PROCURAR NOS VIZINHOS SE TEM ALGUEM BLOQUEANDO
                    block += h2.block
                enlace(h, block, host, pacote)

            else:
                print("\t\tHost " +str(h.id)+ " falha de enlace, redescobrindo as rotas")
                #ALGORITMO DE PROCURA DE VIZINHANÇA AQUI (REDES)
            
        else:
            print("\t\tHost " +str(h.id)+ " nao tem nada para enviar")

        aux = 0
        for p in h.entryBox:
            if(p.destino == h.id):
                #print("\t\tpacote " + str(p.message)+ " entrado em " +str(h.id)+ " chegou ao destino final correto ")
                h.entryBox.pop(aux)
            else:
                print("\t\tpacote " + str(p.message)+ " entrado em " +str(h.id)+ " tem outro destino ")
                pack = h.entryBox.pop(aux)
                pack.origin = h.id
                h.pacote.append(pack)
            aux += 1
    
    for p in pacote:
        ctrl1 += p.status
        if(ctrl1 > 0):
            break
    for h in host:
        h.block = 0
        h.surdo = False
        print("\tHost "+str(h.id)+ " está em status = "+str(h.statusEnlace))
        if(h.statusEnlace > 1):
            ctrl2 = 1

    if(ctrl1 or ctrl2):
        stillGoing = 1
    else:
        stillGoing = 0
    
    round += 1
    
    if(round == 17):
        break