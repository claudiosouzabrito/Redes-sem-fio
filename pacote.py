class Pacote:

    def __init__(self, id, origin, destino, message):
        self.id = id
        self.origin = origin
        self.destino = destino
        self.message = message
        self.status = 1   # 1 = em operação, 0 = resolvido
        self.indo = -1   # -1 = parado, n = id do host q ele ta indo no momento
        self.oldIds = []
        self.jaClonado = 0


