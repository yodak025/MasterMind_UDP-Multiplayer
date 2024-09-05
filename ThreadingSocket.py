import threading
from MMClass import MasterMindGame
from functools import reduce

#Error de recibir de cliente equivocado con MMG.Round

class GameThread (threading.Thread):

    type = {}
    untype = {}
                            #Diccionario con las distintas cabeceras
    messageType = ""                            #Cabecera

    MasterMindGame: MasterMindGame = None       #Clase MasterMind

    secretKeyMessage = ""
    keyTotestMessage = ""

    turns = ""
    keyLength = 4

    def __init__(self, P1, P2):

        threading.Thread.__init__(self)
        self.socketP1 = clientSocket
        self.addressP2 = address
        self.socketP2 = clientSocket
        self.addressP2 = address
        self.GameID = clientSocket
        self.buffer =""

        self.type["Wait"]           = "W"
        self.type["Key"]            = "K"
        self.type["Round Start"]    = "RS"
        self.type["Turn"]           = "T"
        self.type["Game Over"]      = "GO"
        self.type["Error"]          = "E"

        self.untype["K"]      = "Key"
        self.untype["T"]      = "Turn"





    def Encoder(self):                                          #Se ocupa de preparar los mensajes que seran enviados

        type = self.messageType
        message = self.type[self.messageType]


        def keyPackager():                                      #Convierte las claves MM para enviarlas como parte del mensaje
            #match self.MasterMindGame
            if self.secretKeyMessage == "":
                self.secretKeyMessage = reduce((lambda x, y: x + y),
                        map(lambda x: "#" + str(x), self.MasterMindGame.secretCode))

            self.keyTotestMessage = reduce((lambda x, y: x + y),
                    map(lambda x: "#" + str(x), self.MasterMindGame.keyToTest))


        match type:

            case "Init":
                message = message + "#" + "La conexión ha sido un éxito."

            case"SecretKey":
                message = message + "#" + "Se ha configurado tu clave secreta."

            case "Turn":
                keyPackager()
                message = message + self.keyTotestMessage + "#" + str(self.MasterMindGame.currentTurn) + "#" \
                    + str(self.MasterMindGame.exactMatches) + "#" + str(self.MasterMindGame.partialMatches)

            case "Error":
                message = message + "#" + self.error

            case "GameOver":
                keyPackager()
                message = message + self.secretKeyMessage + self.keyTotestMessage + "#" \
                    + str(self.MasterMindGame.currentTurn) + "#" + str(self.MasterMindGame.exactMatches) + "#" + str(self.MasterMindGame.partialMatches)

            case "Win":
                message = message + "#" + "You win!"

        return message





    def Decoder(self):                  #Interpreta los mensajes recibidos

        content = self.buffer.split("#")

        match content[0]:

            case "I":
                try:
                    self.turns = int(content[1])
                except:
                    self.error = "NumberOfTurnsError"
                    self.turns = 10
                    self.messageType = "Error"
                    return
                if self.turns < 150 and self.turns > 0:
                    self.messageType = "Init"
                else:
                    self.error = "NumberOfTurnsError"
                    self.turns = 10
                    self.messageType = "Error"
                return

            case "K":
                self.messageType = self.MasterMindGame.newturn(content[1])
                self.error = self.MasterMindGame.error

            case "SK":
                if len(content[1]) == self.keyLength:
                    self.MasterMindGame = MasterMindGame(combiCode=content[1], turns=self.turns)
                    if self.MasterMindGame.error == "":
                        self.messageType = "SecretKey"
                    else:
                        self.messageType = "Error"
                        if self.MasterMindGame.error == "ColorError":
                            self.error = "SecretKeyError"
                        else:
                            self.error = self.MasterMindGame.error
                else:
                    self.MasterMindGame = MasterMindGame(combiCode="", turns=self.turns)
                    self.messageType = "Error"
                    self.error = "SecretKeyError"







    def run(self):
#Fase 1
        self.buffer = self.socket.recv(1024).decode()
        self.Decoder()
        self.socket.send(self.Encoder().encode())
#Fase 2
        self.buffer = self.socket.recv(1024).decode()
        self.Decoder()
        self.socket.send(self.Encoder().encode())
#Fase 3
        while not self.MasterMindGame.GameOver:
            self.buffer = self.socket.recv(1024).decode()
            self.Decoder()
            self.socket.send(self.Encoder().encode())
