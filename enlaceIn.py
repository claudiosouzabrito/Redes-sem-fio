import logging
from redesIn import rPackage, rReply, rRequest


def checagem(pacote, hostChegada, host, pacotes):  #decide se o pacote será ignorado ou não
    if(pacote.message == 'ACK'):    #caso o pacote seja ack, tira o destinatario da espera, e o mesmo apaga a memoria do pacote que enviou
        hostChegada.ackWait = 0
        #print(str(hostChegada.id)+" com ackWait indo para 0")
        hostChegada.statusEnlace = 0
        hostChegada.pacote.pop(0)
        host[pacote.origin].ackAlvo = -1
        logging.info("(ENLACE)\t\t\t\tAck recebido, eliminando pacote do topo da lista")
        return True
    else:
        if(hostChegada.statusEnlace != 1 or (hostChegada.statusEnlace == 1 and pacote.origin == hostChegada.pckAlvo)): # Recebe qualquer pacote que não seja ack. Caso o destinatario não
                                                                                                                       # esteja a espera de ack, ou ele esteja, mas o host que deveria enviar 
                                                                                                                       # o ack, é quem esta enviando esse pacote atual
            hostChegada.statusEnlace = 2 # vai mandar o ACK 
            logging.info("(ENLACE)\t\t\t\tHost entrando em modo de ACK")
            hostChegada.surdo = True
            logging.info("(ENLACE)\t\t\t\tIncapaz de receber qualquer outro pacote esse round")
            hostChegada.ackAlvo = pacote.origin
            if(pacote.message[:4] == 'RREQ'): #caso o pacote seja um RREQ
                rRequest(pacote, hostChegada, pacotes)

            elif(pacote.message[:4] == 'RREP'): #caso o pacote seja um RREP
                rReply(pacote, hostChegada, pacotes)   
                 
            else:                              #caso seja outro pacote
                rPackage(pacote, hostChegada, host) 

            return True
        else:
            logging.info("(ENLACE)\t\t\t\t\tMas foi bloqueado pois o mesmo estava esperando um ACK")
            return False




    