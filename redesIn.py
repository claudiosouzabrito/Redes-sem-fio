import copy
import uuid
from pacote import Pacote


def rRequest(pacote, hostChegada, host, pacotes):  

    pacote.message += ","+str(hostChegada.id)
    if(len(hostChegada.rotas[int(pacote.message[5])]) == 0):   #Coloca a rota armazenada na cash
            caminho = pacote.message[9:].split(",")
            for i in caminho[::-1]:
                hostChegada.rotas[int(pacote.message[5])].append(int(i))
    print("\t\t\tAdicionando o caminho: "+str(hostChegada.rotas[int(pacote.message[5])])+" no host "+str(hostChegada.id))

    if(str(hostChegada.id) == pacote.message[7]):      #destinatario final
        newId = uuid.uuid4()
        print("\t\t\tRREQ de "+str(pacote.message[5])+" chegou em "+str(pacote.message[7]))

        for idH in hostChegada.vizinho:    #criando os primeiros RREP
            rrep = Pacote(newId, hostChegada.id, idH, "RREP:"+pacote.message[7]+"-"+pacote.message[5]+":"+pacote.message[9:])
            rrep.oldIds.append(hostChegada.id)
            pacotes.append(rrep)

            if(hostChegada.statusEnlace == 1):
                hostChegada.pacote.append(rrep)
            else:
                hostChegada.pacote.insert(0, rrep)

        return False

        
    elif(pacote.id not in hostChegada.oldIds):     #destinatario intermediario
        hostChegada.oldIds.append(pacote.id)
        print("\t\t\tRREQ de "+str(pacote.message[5])+" chegou em um intermediario")

        for idH in hostChegada.vizinho:   #recaminhando para os vizinhos
            if(idH not in pacote.oldIds):   #caso ja não tenha passado por esses hosts 
                rreq = Pacote(pacote.id, hostChegada.id, idH, pacote.message)
                rreq.oldIds = copy.deepcopy(pacote.oldIds)
                rreq.oldIds.append(hostChegada.id)
                pacotes.append(rreq)

                if(hostChegada.statusEnlace == 1): #o host q espera um ack, após 2 rounds sem a resposta (ack), reenvia o pacote anterior
                    hostChegada.pacote.append(rreq)
                else:
                    hostChegada.pacote.insert(0, rreq)

        return True

def rReply(pacote, hostChegada, host, pacotes):
    if(pacote.id not in hostChegada.oldIds):       #se nao é repetido
        hostChegada.oldIds.append(pacote.id)

        if(pacote.message[7] == str(hostChegada.id)):   #se ele chegou no destinatario
            rotaFinal = pacote.message[9:].split(",")
            while(len(rotaFinal) >= 2):                 #colocando a rota principal e as intermediarias 
                hostChegada.rotas[int(rotaFinal[-1])] = copy.deepcopy(rotaFinal) 
                print("\t\t\tAdicionando o caminho: "+str(hostChegada.rotas[int(rotaFinal[-1])])+" no host "+str(hostChegada.id))
                rotaFinal.pop(-1)
            return False

        else:  #RREp chegou em um intermediario
            print("\t\t\tRREQ de "+str(pacote.message[5])+" chegou em um intermediario")
            for idH in hostChegada.vizinho:   
                if(idH not in pacote.oldIds): #repassando para os que não receberam ainda
                    rrep = Pacote(pacote.id, hostChegada.id, idH , pacote.message)
                    rrep.oldIds = copy.deepcopy(pacote.oldIds)
                    rrep.oldIds.append(hostChegada.id)

                    pacotes.append(rrep)
                    if(hostChegada.statusEnlace == 1): #o host q espera um ack, após 2 rounds sem a resposta (ack), reenvia o pacote anterior
                        hostChegada.pacote.append(rrep)
                    else:
                        hostChegada.pacote.insert(0, rrep)
            return True
    


            




    