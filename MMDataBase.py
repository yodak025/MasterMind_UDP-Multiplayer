from MMClass import MasterMindGame
# Creamos la clase node

class node:


    def __init__(self, next=None, socket=None, address=None, playerID=None, gameID = None, started = False):

        self.socket     = socket        #<ip>
        self.address    = address       #<puerto>
        self.playerID   = playerID      #<nombre del jugador>
        self.gameID     = gameID        #<ID de partida>
        self.started    = started       #<para saber si una partida está empezada>
        self.next       = next          #<referencia al siguiente nodo>



class dataBase:

    MMD = {}                                            #Diccionario de las instancias MasterMind
    playersCount = 0                                    #Varible que asigna un gameID a cada instancia MM

    def __init__(self):
        self.head = None

                                                        # Método para agregar elementos en el frente de la linked list

    def addFront(self, socket, address, playerID, gameID=None, started=False):
        self.head = node(socket=socket, address=address, playerID=playerID, next=self.head, gameID=gameID, started=started)


    def eraseMMD(self, gameID):                         #Esto para borrar la instancia MM de MMD
        self.MMD[gameID] = None

    def eraseNode(self, playerID):
        curr = self.head
        prev = None
        while curr and curr.playerID != playerID:
            prev = curr
            curr = curr.next
        if prev is None:
            self.head = curr.next
        elif curr:
            prev.next = curr.next
            curr.next = None

    def replace(self, socket, address, playerID, gameID, started=False):
        self.eraseNode(playerID)
        self.addFront(socket, address, playerID, gameID, started)

                                                        #Método para encontrar un nodo concreto con el nombre del jugador

    def found(self, playerID):                          #Devuleve la información del nodo
        point = self.head
        while point and point.playerID != playerID:
            point = point.next
        return point

        #Otra forma
        #while point != None:
        #    if point.playerID == playerID:
        #        return point
        #    point = point.next
        #return point


                                                        #Método para crear partida usando el nombre del jugador1:
                                                            # añade una instancia MM a MMD
                                                            # cambia el gameID al valor de playersCount.

    def createGame(self, playerID):
        encounter = self.found(playerID)
        self.playersCount += 1
        self.replace(encounter.socket, encounter.address, encounter.playerID, self.playersCount)


                                                        #Método para añadir a la partida un segundo jugador:

    def appendJ2(self, P1, P2):

        player1 = self.found(P1)
        player2 = self.found(P2)

        self.replace(player1.socket, player1.address, player1.playerID, player1.gameID, started=True)
        self.replace(player2.socket, player2.address, player2.playerID, player1.gameID, started=True)


                                                        #Comparador de nombre
                                                            #Recorre la lista
                                                            #Según si encuentra un nombre o no devuelve repeat(bool)

    def comparator(self, playerID):
        repeated = False
        follow = self.head
        while follow != None:
            if playerID == follow.playerID:
                repeated = True
                return repeated
            follow = follow.next
        return repeated


                                                        #Devuelve la lista de las partidas

    def sendData(self):
        subsequent = self.head
        data = ''
        while subsequent != None:
            if not subsequent.started:
                name = subsequent.playerID
                turns = self.MMD[subsequent.gameID].maxTurns
                data += '#' + name + '¬' + str(turns)
            subsequent = subsequent.next
        return data


    def turnRegister(self, P1, nOfTurns):
        self.MMD[self.found(P1).gameID] = MasterMindGame(turns=nOfTurns)




