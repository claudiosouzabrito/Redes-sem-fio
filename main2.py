import copy
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
