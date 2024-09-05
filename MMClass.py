import random


                            # esqueleto inicial
class MasterMindGame:
                            # declaramos las variables que vamos a utilizar

    keyLenght = 4
    MMC = {}                # diccionario de colores válidos.

    Round = "Round 1"

    secretCode1 = []
    secretCode2 = []
                            # código secreto que tenemos que adivinar.
    keyToTest1 = []
    keyToTest2 = []

    validColors = "rgybkw"  # colores mastermind permitidos

    maxTurns = 10           # máximo número de turnos para acertar la clave.
    currentTurn1 = 0
    currentTurn2 = 0        # turno actual.
    Win1 = False
    Win2 = False

    partialMatches = 0
    exactMatches = 0

    error = ""

                                        # construimos la función para iniciar la clase
    def __init__(self, turns = 0):
                                        # iniciamos el diccionario de colores
        self.MMC["red"]     = "💔"
        self.MMC["green"]   = "💚"
        self.MMC["yellow"]  = "💛"
        self.MMC["blue"]    = "💙"
        self.MMC["black"]   = "🖤"
        self.MMC["white"]   = "🤍"

        if turns > 0:
             self.maxTurns = turns

    def secretCode(self, Key):
        match self.Round:
            case "Round 1":
                if Key == "" or Key == "noCombiCode" or Key == "nocombiCode":
                    self.secretCode1 = self.randomCode(self.keyLenght)
                elif len(Key) != self.keyLenght:
                    self.secretCode1 = self.randomCode(self.keyLenght)
                    self.error = "SecretKeyError"
                else:
                    try:
                        self.secretCode1 = self.toMasterMindColorCombination(list(Key))
                    except:
                        self.secretCode1 = self.randomCode(self.keyLenght)
                        self.error = "SecretKeyError"
                    if self.error !=  "":
                        self.secretCode1 = self.randomCode(self.keyLenght)


            case"Round 2":
                if Key == "" or Key == "noCombiCode" or Key == "nocombiCode":
                    self.secretCode2 = self.randomCode(self.keyLenght)
                elif len(Key) != self.keyLenght:
                    self.secretCode2 = self.randomCode(self.keyLenght)
                    self.error = "SecretKeyError"
                else:
                    try:
                        self.secretCode2 = self.toMasterMindColorCombination(list(Key))
                    except:
                        self.secretCode2 = self.randomCode(self.keyLenght)
                        self.error = "SecretKeyError"
                    if self.error != "":
                        self.secretCode2 = self.randomCode(self.keyLenght)






    def randomCode(self, n: int):   # genera un código aleatorio

        colorlist = list(self.validColors)
        passCode = random.choices(colorlist, k=n)

        self.RandomCode = True

        return self.toMasterMindColorCombination(passCode)



    def MasterMindColor(self, color: str):  # convertir cadenas en colores
        rcolor = "Color no encontrado."

        if   color == "r" or color == "R" or color == "💔":
             rcolor = self.MMC["red"]
        elif color == "g" or color == "G" or color == "💚":
             rcolor = self.MMC["green"]
        elif color == "b" or color == "B" or color == "💙":
             rcolor = self.MMC["blue"]
        elif color == "y" or color == "Y" or color == "💛":
             rcolor = self.MMC["yellow"]
        elif color == "k" or color == "K" or color == "🖤":
             rcolor = self.MMC["black"]
        elif color == "w" or color == "W" or color == "🤍":
             rcolor = self.MMC["white"]
        else:
            self.error = "ColorError"

        return rcolor



    def toMasterMindColorCombination(self, combi: list):  # obtener una cadena de colores mastermind
        return list(map(lambda n: self.MasterMindColor(n), combi))




    def countExactMatches(self, keyToTest: list):
        compResult = []
        match self.Round:
            case "Round 1":
                compResult = list(map(lambda x, y: x == y, keyToTest,self.secretCode1))
            case "Round 2":
                compResult = list(map(lambda x, y: x == y, keyToTest, self.secretCode2))
        count = len(list(filter(lambda x: x is True, compResult)))
        self.exactMatches = count



    def countPartialMatches(self, keyToTest: list):

        count = 0
        both = []


        match self.Round:
            case "Round 1":
                both = list(map(lambda x, y: (x, y), keyToTest, self.secretCode1))
            case "Round 2":
                both = list(map(lambda x, y: (x, y), keyToTest, self.secretCode2))

        bothWithoutsExactMatches    = list(filter(lambda x: x[0] is not x[1], both))
        keyWithoutExactMatches      = list(map(lambda x: x[0], bothWithoutsExactMatches))
        codeWithoutExactMatches     = list(map(lambda x: x[1], bothWithoutsExactMatches))

        for key in keyWithoutExactMatches:
            for code in codeWithoutExactMatches:
                if key == code:
                    count += 1
                    codeWithoutExactMatches.remove(code)
                    break

        self.partialMatches = count



    def GameOver(self):
        if self.currentTurn1 < self.currentTurn2:
            self.Win1 = True
        if self.currentTurn1 > self.currentTurn2:
            self.Win2 = True

        return "Game Over"




    def newturn(self, Key):                         #NewTurn ahora devuelve las cabeceras y almacena los errores que se generan en el programa
        self.error = ""


        match self.Round:

            case "Round 1":
                try:
                    self.keyToTest1 = self.toMasterMindColorCombination(Key)
                    self.countExactMatches(self.keyToTest1)
                    self.countPartialMatches(self.keyToTest1)
                except:
                    return "Error"

                if self.error != "":
                    self.error = "KeyError"
                    return "Error"

                if len(self.keyToTest1) != self.keyLenght:
                    self.error = "KeyError"
                    return "Error"

                self.currentTurn1 += 1
                if self.keyToTest1 == self.secretCode1 or self.currentTurn1 == self.maxTurns:
                    return "Round Finish"


                return "Turn"


            case "Round 2":
                try:
                    self.keyToTest2 = self.toMasterMindColorCombination(Key)
                    self.countExactMatches(self.keyToTest2)
                    self.countPartialMatches(self.keyToTest2)
                except:
                    return "Error"

                if self.error != "":
                    self.error = "KeyError"
                    return "Error"

                if len(self.keyToTest2) != self.keyLenght:
                    self.error = "KeyError"
                    return "Error"

                self.currentTurn2 += 1
                if self.keyToTest2 == self.secretCode2 or self.currentTurn2 == self.maxTurns:
                    return "Round Finish"

                return "Turn"


