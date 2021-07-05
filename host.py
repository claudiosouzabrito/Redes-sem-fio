class Host:

    def __init__(self, id, x, y, range):
        self.id = id
        self.x = x
        self.y = y
        self.range = range
        self.pacote = []
        self.entryBox = []
        self.ready2send = 1
        self.statusEnlace = 0
        self.block = 0
        self.ackAlvo = -1
        self.ackWait = 0
        self.surdo = False
        self.pckAlvo = -1
        self.vizinho = []
        self.rotas = []
        self.oldIds = []
        self.rrepWait = 0
