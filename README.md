# Redes-sem-fio
Simulação de redes sem fio usando Python

Projeto de Redes sem Fio

Neste projeto a equipe deverá implementar as camadas físicas, de enlace e de rede de uma rede sem fio. O
objetivo é criar uma simulação de rede sem fio onde pacotes saiam de uma origem e cheguem a um
destino, não importando o número de nós intermediários.
Especificação:

• Na simulação devem existir obrigatoriamente as entidades roteador, pacote e hospedeiro (host).
Outras entidades podem existir conforme a necessidade;

• Deve-se implementar algum protocolo de roteamento de redes sem fio para redes ad hoc (redes
de sensores, VANETs, MANETs, FANETs, redes mesh, etc);

• Deve-se implementar o controle de acesso ao meio (camada de enlace).

• Deve-se implementar uma forma de transmissão de um pacote entre entidades (função da
camada física). Pode ser uma estratégia simples;

• Deve-se implementar o conceito de encapsulamento do pacote entre as camadas;

• A quantidade de cada de entidade (pacote, roteador e hospedeiro) deve ser configurável;

• Deve-se implementar alguma forma de disposição dos nós em um ambiente (aleatória, matriz,
etc);

• A simulação deve permitir seja definido a quantidade N de pacotes a serem transmitidos entre
uma origem S e um destino D. O caminho para cada pacote será definido conforme o protocolo
de roteamento escolhido.

• Deve-se implementar alguma forma de visualização das rotas e do encaminhamento dos pacotes.

• A simulação deve gerar log com o resultado do encaminhamento para análise.

Observações:
Ao implementar qualquer função, lembrem-se que estão trabalhando com redes sem fio. Por isso tenham
em mente as seguintes observações:

• A transmissão é sempre broadcast. A diferença é que apenas alguns recebem

• Podem ocorrer colisões;

• O alcance do rádio é limitado, por isso distância entre nós importa.

• Enlaces podem falhar devido à mobilidade e energia dos nós.

• Antes do roteamento, os nós precisam descobrir os seus vizinhos

O que será avaliado:

• Se o aluno implementou de fato as camadas

• Se o pacote segue o caminho definido

• Se o caminho é recalculado em caso de falhas de enlaces

• Presença de descrição e justificativa de todas as decisões tomadas
