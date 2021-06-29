from graph import graph
from host import Host 
import json
from pacote import Pacote

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
    pck = Pacote(i, jay["origin"], jay["destino"], jay["mesage"])
    print('\tid: ' +str(i)+ ', origin: ' + str(pck.origin) + ', destino: ' + str(pck.destino) + ', mensagem: ' + str(pck.mesage))
    pacote.append(pck)

    host[jay["origin"]].pacotes.append(pck)

round = 0
graph(x,y,ranges, nomes, numHost, dimension, round)
print("\nRound "+str(round))
print("\tStatus:")
for h in host:
    if(len(h.pacotes) == 0):
        print("\t\tHost " +str(h.id)+ " não tem pacote nenhum para mandar")
    else:
        for p in h.pacotes:
            print("\t\tHost " +str(h.id)+ "possui os seguintes pacotes para enviar: ")
            print("\t\t\t" + p.mesage)