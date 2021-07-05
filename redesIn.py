import copy
import uuid
from pacote import Pacote


def rRequest(pacote, hostChegada, host, pacotes):  

    message = pacote.message +","+str(hostChegada.id)

    if(len(hostChegada.rotas[int(pacote.message[5])]) == 0):   #Coloca a rota armazenada na cash
        caminho = message[9:].split(",")
        print("\t\t\tAdicionando o caminho: "+str(caminho)+" no host "+str(hostChegada.id))
        for i in caminho[::-1]:
            hostChegada.rotas[int(pacote.message[5])].append(int(i))
    else:
        print("\t\t\tHost "+str(hostChegada.id)+ " ja tem caminho para "+str(hostChegada.rotas[int(pacote.message[5])]))
    
    if(pacote.id not in hostChegada.oldIds):  #se eu ja não recebi esse pacote antes
        hostChegada.oldIds.append(pacote.id)
        
        if(str(hostChegada.id) == pacote.message[7]):      #destinatario final
            
            newId = uuid.uuid4()
            print("\t\t\tRREQ de "+str(pacote.message[5])+" chegou em "+str(pacote.message[7])+" destinatario final. Criando RREP para vizinhos")

            for idH in hostChegada.vizinho:    #criando os primeiros RREP
                rrep = Pacote(newId, hostChegada.id, idH, "RREP:"+pacote.message[7]+"-"+pacote.message[5]+":"+message[9:])
                rrep.oldIds.append(hostChegada.id)
                pacotes.append(rrep)

                if(hostChegada.statusEnlace == 1):
                    hostChegada.pacote.append(rrep)
                else:
                    hostChegada.pacote.insert(0, rrep)
            
        else:     #destinatario intermediario
            
            print("\t\t\tRREQ de "+str(pacote.message[5])+" chegou em um intermediario")

            for idH in hostChegada.vizinho:   #recaminhando para os vizinhos
                if(idH not in pacote.oldIds):   #caso ja não tenha passado por esses hosts 
                    print("\t\t\t\tRREQ futuramente encaminhado para "+str(idH))
                    rreq = Pacote(pacote.id, hostChegada.id, idH, message)
                    rreq.oldIds = copy.deepcopy(pacote.oldIds)
                    rreq.oldIds.append(hostChegada.id)
                    pacotes.append(rreq)

                    if(hostChegada.statusEnlace == 1): #o host q espera um ack, após 2 rounds sem a resposta (ack), reenvia o pacote anterior
                        hostChegada.pacote.append(rreq)
                    else:
                        hostChegada.pacote.insert(0, rreq)


def rReply(pacote, hostChegada, host, pacotes):
    if(pacote.id not in hostChegada.oldIds):       #se nao é repetido
        hostChegada.oldIds.append(pacote.id)

        if(pacote.message[7] == str(hostChegada.id)):   #se ele chegou no destinatario
            print("\t\t\tRREP chegou no destinatario final")
            rotaFinal = pacote.message[9:].split(",")
            rotaFinal = [int(x) for x in rotaFinal]

            while(len(rotaFinal) >= 2):                 #colocando a rota principal e as intermediarias 
                hostChegada.rotas[int(rotaFinal[-1])] = copy.deepcopy(rotaFinal) 
                print("\t\t\t\tAdicionando o caminho: "+str(hostChegada.rotas[int(rotaFinal[-1])])+" no host "+str(hostChegada.id))
                rotaFinal.pop(-1)

            hostChegada.rrepWait = 0

        else:  #RREp chegou em um intermediario
            print("\t\t\tRREP de "+str(pacote.message[5])+" chegou em um host que nao eh o alvo final do pacote")
            for idH in hostChegada.vizinho:   
                if(idH not in pacote.oldIds): #repassando para os que não receberam ainda
                    print("\t\t\t\tRREP futuramente encaminhado para "+str(idH))
                    rrep = Pacote(pacote.id, hostChegada.id, idH , pacote.message)
                    rrep.oldIds = copy.deepcopy(pacote.oldIds)
                    rrep.oldIds.append(hostChegada.id)

                    pacotes.append(rrep)
                    if(hostChegada.statusEnlace == 1): #o host q espera um ack, após 2 rounds sem a resposta (ack), reenvia o pacote anterior
                        hostChegada.pacote.append(rrep)
                    else:
                        hostChegada.pacote.insert(0, rrep)


def rPackage(pacote, hostChegada, host, pacotes):
    if(pacote.id not in hostChegada.oldIds):       #se nao é repetido
        hostChegada.oldIds.append(pacote.id)


        if(pacote.message[2] == str(hostChegada.id)):   #se ele chegou no destinatario
            print("\t\t\tPacote chegou no destinatario final")
            

        else:  #pacote chegou em um intermediario

            if(hostChegada.id in host[int(pacote.message[0])].rotas[int(pacote.message[2])]):
                print("\t\t\tPacote "+str(pacote.message)+" chegou em um intermediario")
                print("\t\t\tPacote futuramente encaminhado para os vizinhos")
                pacotecopia = Pacote(pacote.id, hostChegada.id, int(pacote.message[2]), pacote.message)
                pacotecopia.oldIds = copy.deepcopy(pacote.oldIds)
                pacotecopia.oldIds.append(hostChegada.id)

                hostChegada.pacote.append(pacotecopia)
            else:
                print("\t\t\tPacote "+str(pacote.message)+" sera ignorado pelo host pois nao faz parte da rota")

                    


            




    