class Host:

    def __init__(self, id, x, y, range):
        self.id = id
        self.x = x
        self.y = y
        self.range = range
        self.pacote = []
        self.entryBox = []
        self.ready2send = 0
        self.statusEnlace = 0
        self.freeze = 0
        self.rtsAlvo = -1
        self.ctsAlvo = -1
