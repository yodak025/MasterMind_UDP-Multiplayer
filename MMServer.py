import threading
from MMDataBase import dataBase
import sys, getopt
from functools import reduce
from newSocket import *



playerIDErrorCount = 0



class MasterMindServer():                #Gestiona la conexión TCP

    def __init__(self, serverName, serverPort): #añadir ip
        self.serverName = serverName
        self.serverPort = serverPort
        self.serverSocket = None



    def activate(self):
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind((self.serverName, self.serverPort))
        self.serverSocket.listen(1) # Numero de solicitudes en cola admitidas, resto se descartan


    def comunication(self):
        while True:
            (socket, address) = self.serverSocket.accept()
            linkinThread = LinkinThread(socket, address)
            print(f"Conexión desde: {address}")

            try:
                linkinThread.start()

            except ValueError:
                self.close()


    def close(self):
        self.serverSocket.close()




class arguments():              #Clase encargada de leer los argumentos escritos en el terminal

    ip = ""
    port = 0

    selfportError: bool
    ipError: bool

    def __init__(self):
        (opts, args) = getopt.getopt(sys.argv[1:], "i:p:", ["ip=", "port="])
        for o, a in opts:
            if o in ("-i", "--ip"):
                self.ip = a
            elif o in ("-p", "--port"):
                self.port = a

        self.portError = False
        self.ipError = False


    def argumentError(self):

        if len(self.ip) == 0:
            self.ipError =True
        else:
            try:
                self.port = int(self.port)
                if self.port < 1:
                    self.portError = True
            except ValueError:
                self.portError = True


    def argumentRun(self):                      #Gestion de errores
        if self.ipError:
            print("Error:InvalidInput_type=ip")
            self.ip = "127.0.0.1"
        if self.portError:
            print("Error:InvalidInput_type=port")
            self.port = 1234
        else:
            print("Argumentos correctos.")




class LinkinThread(threading.Thread):

    messageType: str = None

    type = {}
    untype = {}
    clientType: str = None
    buffer: str = None

    playerID: str = None

    error: str = None

    Game = None

    def __init__(self, socket, address):

        threading.Thread.__init__(self)

        self.socket = newSocket(socket)
        self.address = address

        self.type["Turn Select"]    = "TS"
        self.type["Wait"]           = "W"
        self.type["Games"]          = "G"
        self.type["Error"]          = "E"

        self.untype["M"]    = "Menu"
        self.untype["TS"]   = "Turn Select"
        self.untype["G"]    = "Game"

    def Encoder(self):

        message = self.type[self.messageType]

        match self.messageType:

            case "Turn Select":
                pass
            case "Games":
                message += dataBase.sendData()
            case "Wait":
                message += "#MA"
            case "Error":
                message += self.error
                self.messageType = ""
                self.error = ""

        return message

    def Decoder(self):
        content = self.buffer.split("#")
        content[0] = self.untype[content[0]]

        match content[0]:

            case "Menu":

                if dataBase.comparator(content[2]):
                    global playerIDErrorCount
                    self.messageType = "Error"
                    playerIDErrorCount += 1
                    self.error = f"NameInUseError#{content[2]}{str(playerIDErrorCount)}"
                    self.playerID = content[2] + str(playerIDErrorCount)

                else:
                    self.playerID = content[2]

                match content[1]:
                    case "P1":
                        dataBase.addFront(socket=self.socket, address=self.address, playerID=self.playerID)
                        self.clientType = "Player 1"
                        self.messageType = "Turn Select"
                        dataBase.createGame(self.playerID)
                    case "P2":
                        dataBase.addFront(socket=self.socket, address=self.address, playerID=self.playerID, started=True)
                        self.clientType = "Player 2"
                        self.messageType = "Games"

            case "Turn Select":
                try:
                    turns = int(content[1])
                except:
                    self.error = "NumberOfTurnsError"
                    self.messageType = "Error"
                    turns = 10
                if turns < 150 and turns > 0 and self.messageType != "Error":
                    self.messageType = "Wait"
                else:
                    self.error = "NumberOfTurnsError"
                    self.messageType = "Error"
                    turns = 10
                dataBase.turnRegister(P1=self.playerID, nOfTurns=turns)


            case "Game":
                dataBase.appendJ2(P1=content[1], P2=self.playerID)
                self.Game = Game(P1=content[1], P2=self.playerID)

        return


    def run(self):

        #recibe menu, registra, decide si es P1 (creando la partida) o P2 y responde select turn o games
        self.buffer = self.socket.recv(1024).decode()
        self.Decoder()
        self.socket.send(self.Encoder().encode())


        match self.clientType:

            #recibe select turn, actualiza maxturns, responde wait(match
            case "Player 1":
                self.buffer = self.socket.recv(1024).decode()
                self.Decoder()
                self.socket.send(self.Encoder().encode())

            case "Player 2":
                self.buffer = self.socket.recv(1024).decode()
                self.Decoder()
                self.Game.MasterMindGame()




class Game():

    type = {}
    untype = {}

    messageType = ""

    secretKey1Message = ""
    secretKey2Message = ""
    keyTotestMessage = ""

    buffer: str = None

    ack = False
    validSecretKey = False

    def __init__(self, P1, P2):

        self.playerP1 = dataBase.found(P1).playerID
        self.socketP1   = dataBase.found(P1).socket
        self.addressP1  = dataBase.found(P1).address

        self.playerP2 = dataBase.found(P2).playerID
        self.socketP2   = dataBase.found(P2).socket
        self.addressP2  = dataBase.found(P2).address

        self.GameID     = dataBase.found(P1).gameID

        self.type["Wait"]           = "W"
        self.type["Key"]            = "K"
        self.type["Round Start"]    = "RS"
        self.type["Turn"]           = "T"
        self.type["Round Finish"]   = "RF"
        self.type["Game Over"]      = "GO"
        self.type["Error"]          = "E"

        self.untype["K"] = "Key"
        self.untype["T"] = "Turn"





    def Encoder(self, Player = None):                                          #Se ocupa de preparar los mensajes que seran enviados

        type = self.messageType
        message = self.type[self.messageType]


        def keyPackager():                                      #Convierte las claves MM para enviarlas como parte del mensaje
            match dataBase.MMD[self.GameID].Round:
                case "Round 1":
                    if self.secretKey1Message == "":
                        self.secretKey1Message = reduce((lambda x, y: x + y),
                                                        map(lambda x: "#" + str(x), dataBase.MMD[self.GameID].secretCode1))

                    self.keyTotestMessage = reduce((lambda x, y: x + y),
                                                        map(lambda x: "#" + str(x), dataBase.MMD[self.GameID].keyToTest1))

                case "Round 2":
                    if self.secretKey2Message == "":
                        self.secretKey2Message = reduce((lambda x, y: x + y),
                                                       map(lambda x: "#" + str(x),dataBase.MMD[self.GameID].secretCode2))

                    self.keyTotestMessage = reduce((lambda x, y: x + y),
                                                       map(lambda x: "#" + str(x), dataBase.MMD[self.GameID].keyToTest2))


        match type:

            case "Wait":
                match dataBase.MMD[self.GameID].Round:
                    case "Round 1":
                        message += "#R1"
                    case "Round 2":
                        message += "#R2"

            case "Key":
                if self.ack:
                    if self.validSecretKey:
                        message += "#ACK#T"
                    else:
                        message += "#ACK#F"
                else:
                    match dataBase.MMD[self.GameID].Round:
                        case "Round 1":
                            message += "#R1"
                        case "Round 2":
                            message += "#R2"

            case "Round Start":
                pass

            case "Turn":
                keyPackager()
                match dataBase.MMD[self.GameID].Round:
                    case "Round 1":
                        message = message + self.keyTotestMessage + "#" + str(dataBase.MMD[self.GameID].currentTurn1) + "#" \
                            + str(dataBase.MMD[self.GameID].exactMatches) + "#" + str(dataBase.MMD[self.GameID].partialMatches)
                    case "Round 2":
                        message = message + self.keyTotestMessage + "#" + str(dataBase.MMD[self.GameID].currentTurn2) + "#" \
                            + str(dataBase.MMD[self.GameID].exactMatches) + "#" + str(dataBase.MMD[self.GameID].partialMatches)

            case "Round Finish":
                keyPackager()
                match dataBase.MMD[self.GameID].Round:
                    case "Round 1":
                        dataBase.MMD[self.GameID].Round = "Round 2"
                        if dataBase.MMD[self.GameID].keyToTest1 == dataBase.MMD[self.GameID].secretCode1:
                            message = message + "#V" + self.secretKey1Message + self.keyTotestMessage \
                                              + "#" + str(dataBase.MMD[self.GameID].currentTurn1) \
                                              + "#" + str(dataBase.MMD[self.GameID].exactMatches) \
                                              + "#" + str(dataBase.MMD[self.GameID].partialMatches)
                        else:
                            message = message + "#L" + self.secretKey1Message + self.keyTotestMessage \
                                              + "#" + str(dataBase.MMD[self.GameID].currentTurn1) \
                                              + "#" + str(dataBase.MMD[self.GameID].exactMatches) \
                                              + "#" + str(dataBase.MMD[self.GameID].partialMatches)

                    case "Round 2":
                        dataBase.MMD[self.GameID].Round = "Game Over"
                        if dataBase.MMD[self.GameID].keyToTest2 == dataBase.MMD[self.GameID].secretCode2:
                            message = message + "#V" + self.secretKey2Message + self.keyTotestMessage \
                                              + "#" + str(dataBase.MMD[self.GameID].currentTurn2) \
                                              + "#" + str(dataBase.MMD[self.GameID].exactMatches) \
                                              + "#" + str(dataBase.MMD[self.GameID].partialMatches)
                        else:
                            message = message + "#L" + self.secretKey2Message + self.keyTotestMessage \
                                              + "#" + str(dataBase.MMD[self.GameID].currentTurn2) \
                                              + "#" + str(dataBase.MMD[self.GameID].exactMatches) \
                                              + "#" + str(dataBase.MMD[self.GameID].partialMatches)


            case "Game Over":
                match Player:
                    case "Player 1":
                        if dataBase.MMD[self.GameID].Win1:
                            message += "#V"
                        if dataBase.MMD[self.GameID].Win2:
                            message += "#L"
                        else:
                            message += "#D"
                    case "Player 2":
                        if dataBase.MMD[self.GameID].Win1:
                            message += "#L"
                        if dataBase.MMD[self.GameID].Win2:
                            message += "#V"
                        else:
                            message += "#D"

            case "Error":
                message = message + "#" + dataBase.MMD[self.GameID].error

        return message





    def Decoder(self):                  #Interpreta los mensajes recibidos

        content = self.buffer.split("#")
        content[0] = self.untype[content[0]]
        match content[0]:

            case "Turn":
                self.messageType = dataBase.MMD[self.GameID].newturn(content[1])

            case "Key":
                self.ack = True
                dataBase.MMD[self.GameID].secretCode(content[1])
                if dataBase.MMD[self.GameID].error == "":
                    self.validSecretKey = True





    def MasterMindGame(self):

        self.messageType = "Wait"
        self.socketP1.send(self.Encoder().encode())
        self.messageType = "Key"
        self.socketP2.send(self.Encoder().encode())

        self.buffer = self.socketP2.recv(1024).decode()
        self.Decoder()
        self.socketP2.send(self.Encoder().encode())

        self.messageType = "Round Start"
        self.socketP1.send(self.Encoder().encode())

        while dataBase.MMD[self.GameID].Round == "Round 1":
            self.buffer = self.socketP1.recv(1024).decode()
            self.Decoder()
            self.buffer = self.Encoder()
            self.socketP1.send(self.buffer.encode())
            self.socketP2.send(self.buffer.encode())


        self.ack = False
        self.validSecretKey = False

        self.messageType = "Key"
        self.socketP1.send(self.Encoder().encode())
        self.messageType = "Wait"
        self.socketP2.send(self.Encoder().encode())

        self.buffer = self.socketP1.recv(1024).decode()
        self.Decoder()
        self.socketP1.send(self.Encoder().encode())

        self.messageType = "Round Start"
        self.socketP2.send(self.Encoder().encode())

        while dataBase.MMD[self.GameID].Round == "Round 2":
            self.buffer = self.socketP2.recv(1024).decode()
            self.Decoder()
            self.buffer = self.Encoder()
            self.socketP1.send(self.buffer.encode())
            self.socketP2.send(self.buffer.encode())

        self.messageType = dataBase.MMD[self.GameID].GameOver()
        self.socketP1.send(self.Encoder(Player="Player 1").encode())
        self.socketP2.send(self.Encoder(Player="Player 2").encode())

        dataBase.eraseMMD(self.GameID)
        dataBase.eraseNode(self.playerP1)
        dataBase.eraseNode(self.playerP2)









########################## E J E C U C I O N #####################################



#Se inicia la clase arguments y procesa los datos

arguments = arguments()
arguments.argumentError()
arguments.argumentRun()

dataBase = dataBase()

MasterMindServer = MasterMindServer(arguments.ip, arguments.port)

MasterMindServer.activate()
print ("El servidor esta listo para ser usado")
MasterMindServer.comunication()
MasterMindServer.close()
