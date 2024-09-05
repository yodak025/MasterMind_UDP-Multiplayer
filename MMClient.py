
from subprocess import run as terminal
from time import sleep
import getopt, sys
from newSocket import *






class Client():                                             #Clase encargada de la conexion TCP y de la comunicacion con el servidor

    type = {}
    untype = {}
    buffer = ""
    GameOver: bool
    namelist = []
    content = []
    clientType = ""

    def __init__(self, serverName, serverPort, playerName):
        self.playerName = playerName
        self.serverName = serverName
        self.serverPort = serverPort
        self.clientSocket = None

        self.type["Turn"]       = "T"
        self.type["Key"]        = "K"
        self.type["Menu"]       = "M"
        self.type["TurnSelect"] = "TS"
        self.type["Games"]      = "G"

        self.untype["TS"]       = "TurnSelect"
        self.untype["M"]        = "Menu"
        self.untype["I"]        = "Init"
        self.untype["T"]        = "Turn"
        self.untype["E"]        = "Error"
        self.untype["GO"]       = "GameOver"
        self.untype["V"]        = "Win"
        self.untype["K"]        = "Key"
        self.untype["SK"]       = "SecretKey"
        self.untype["W"]        = "Wait"
        self.untype["MA"]       = "Match"
        self.untype["R1"]       = "Round 1"
        self.untype["R2"]       = "Round 2"
        self.untype["P1"]       = "Player 1"
        self.untype["P2"]       = "Player 2"
        self.untype["G"]        = "Games"
        self.untype["L"]        = "Lose"
        self.untype["D"]        = "Draw"
        self.untype["P"]        = "Player"
        self.untype["RS"]       = "Round Start"
        self.untype["RF"]       = "Round Finish"
        self.untype["ACK"] = "ACK"

        self.GameOver = False
        self.ack = False



    def Encoder(self, type: str, input):                #Genera mensajes para enviar
        buffer = self.type[type] + "#"
        match type:
            case "Menu":
                buffer = buffer + "P" + input + "#" + self.playerName
            case "TurnSelect":
                buffer = buffer + input
            case "Games":
                name =self.namelist[int(input)]
                buffer = buffer + name
            case "Turn":
                buffer = buffer + input
            case "Key":
                buffer = buffer + input
        return buffer



    def Decoder(self, Type = None):         # Interpreta mensajes del servidor e imprime por pantalla

        content = self.buffer.split("#")
        content[0] = self.untype[content[0]]
        self.content = content

        match content[0]:

            case "TurnSelect":              #Recibir TurnSelect es la condición para ser jugador 1

                self.clientType = "Player 1"

            case "Games":                   #Recibir Games es la condición para ser jugador 2


                if self.buffer == "G":
                    print("No hay partidas disponibles en este momento.")
                    print("Intentalo mas tarde.")
                    input("Pulsa enter para continuar.")
                    self.close()
                    exit(-1)

                self.clientType = "Player 2"
                print("🕹: PARTIDAS DISPONIBLES 🕹")
                print("")
                print("(NOMBRE - NºTURNOS)")
                content.pop(0)
                self.namelist.append("SINNOMBRE")

                for i in content:
                    game = i.split("¬")
                    print(f"{content.index(i) + 1}.- ({game[0]} , {game[1]})")
                    self.namelist.append(game[0])


            case "Wait":
                content[1] = self.untype[content[1]]
                match content[1]:
                    case "Match":
                        print("Partida creada")
                        print("Esperando jugador...")
                    case "Round 1":
                        print("Se ha unido un jugador a la sala")
                        print("Esperando clave secreta...")
                    case "Round 2":
                        self.GameOver = True
                        print("Esperando a que el jugador 1 introduzca la clave secreta")

            case "Round Start":
                print("El jugador ya ha introducido una clave secreta. Intenta adivinarla.")
                print("**Clave de colores**")
                print("")
                print("             Rojo     💔  : Letra R")
                print("             Azul     💙  : Letra B")
                print("             Amarillo 💛  : Letra Y")
                print("             Verde    💚  : Letra G")
                print("             Negro    🖤  : Letra K")
                print("             Blanco   🤍  : Letra W")
                print("")


            case "Key":
                content[1] = self.untype[content[1]]
                match content[1]:
                    case "Round 1":
                        print("**Clave de colores**")
                        print("")
                        print("             Rojo     💔  : Letra R")
                        print("             Azul     💙  : Letra B")
                        print("             Amarillo 💛  : Letra Y")
                        print("             Verde    💚  : Letra G")
                        print("             Negro    🖤  : Letra K")
                        print("             Blanco   🤍  : Letra W")
                        print("")

                    case "Round 2":
                        self.GameOver = True
                        print("**Clave de colores**")
                        print("")
                        print("             Rojo     💔  : Letra R")
                        print("             Azul     💙  : Letra B")
                        print("             Amarillo 💛  : Letra Y")
                        print("             Verde    💚  : Letra G")
                        print("             Negro    🖤  : Letra K")
                        print("             Blanco   🤍  : Letra W")
                        print("")

                    case "ACK":
                        if content[2] == "T":
                            print("La clave ha sido configurada con exito")
                        else:
                            print("Error al configurar la clave. Se ha asignado una clave aleatoria")

            case "Turn":
                Key = list(map(lambda x: content[x], range(1, 4 + 1)))
                currentTurn = content[5]
                EMatches = content[6]
                PMatches = content[7]

                match Type:
                    case "Playing":

                        print("")
                        print(f"Tu turno: {currentTurn}")
                        print(f"Tu combinación es: {Key}")
                        print(f"Número de aciertos: {EMatches}")
                        print(f"Número de semiaciertos: {PMatches}")
                        print("")
                        print("No te rindas!")
                        print("")
                        print("")
                    case "Reading":
                        print("")
                        print(f"Su turno: {currentTurn}")
                        print(f"Su combinación es: {Key}")
                        print(f"Número de aciertos: {EMatches}")
                        print(f"Número de semiaciertos: {PMatches}")
                        print("")
                        print("")

            case "Round Finish":
                self.GameOver = True
                match self.untype[content[1]]:
                    case "Win":
                        secretCode = list(map(lambda x: content[x], range(2, 5 + 1)))
                        currentTurn = content[10]

                        match Type:
                            case "Playing":

                                print("")
                                print("Has Ganado !!!!")
                                print(f"Turno: {currentTurn}")
                                print(f"La clave sereta era: {secretCode}")
                                print("")
                                print("")
                            case "Reading":
                                print(f"Tu rival ha acertado la clave secreta {secretCode} en el turno {currentTurn}")
                                print("")
                                print("")



                    case "Lose":
                        secretCode = list(map(lambda x: content[x], range(2, 5 + 1)))
                        key = list(map(lambda x: content[x], range(6, 9 + 1)))
                        EMatches = content[11]
                        PMatches = content[12]
                        match Type:
                            case "Playing":

                                print("")
                                print("Vaya... Se ha terminado la ronda.")
                                print(f"Tu combinación era {key}, y la clave secreta era {secretCode}")
                                print(f"Número de aciertos: {EMatches}")
                                print(f"Número de semiaciertos: {PMatches}")
                                print("")
                                print("")
                            case "Reading":
                                print("")
                                print(f"Tu rival no ha acertado tu clave secreta {secretCode}")
                                print(f"Número de aciertos: {EMatches}")
                                print(f"Número de semiaciertos: {PMatches}")
                                print("")
                                print("")




            case "Error":
                print("")
                match content[1]:
                    case "NameInUseError":
                        print("Se ha producido un error.")
                        print("El nombre que has introducido ya esta siendo utilizado por otro jugador")
                        print(f"Se te ha asignado por defecto el nombre:{content[2]}")
                    case "NumberOfTurnsError":
                        print("Se ha producido un error.")
                        print("El numero que has introducido no es valido.")
                        print("Se han configurado por defecto 10 turnos.")
                    case "SecretKeyError":
                        print("Se ha producido un error.")
                        print("La clave que has introducido no es valida")
                        print("Se ha configurado una clave secreta aleatoria por defecto.")
                        sleep(3)
                    case "KeyError":
                        print("Se ha producido un error.")
                        print("Clave incorrecta.")
                        print("Vuelve a intentarlo!")
                    case other:
                        print("Se ha producido un error.")
                        print("Información sobre el error: error_Type:UnknownError")
                print("")

            case "GameOver":
                content[1] = self.untype[content[1]]
                match content[1]:
                    case "Lose":
                        self.GameOver = True

                        terminal("clear")
                        print("")
                        print("####   ##   #   #  ####       ####  #   #  ####  ### ")
                        print("#     #  #  ## ##  #          #  #  #   #  #     #  #")
                        print("# ##  ####  # # #  ####       #  #  #   #  ####  ### ")
                        print("#  #  #  #  # # #  #          #  #   # #   #     #  #")
                        print("####  #  #  #   #  ####       ####    #    ####  #  #")
                        print("")

                    case "Draw":
                        self.GameOver = True

                        terminal("clear")
                        print("")
                        print("####      ###      ##     #  #  # ")
                        print("#   #     #  #    #  #    #  #  # ")
                        print("#    #    ###     ####    #  #  # ")
                        print("#   #     #  #    #  #     # # #  ")
                        print("####      #  #    #  #      ###   ")
                        print("")

                    case "Win":
                        self.GameOver = True

                        terminal("clear")
                        print("")
                        print("#    #  ####  #  #       #  #  #  ##  ##  # ")
                        print(" #  #   #  #  #  #       #  #  #  ##  ##  # ")
                        print("  ##    #  #  #  #       #  #  #  ##  # # # ")
                        print("  ##    #  #  #  #        # # #   ##  #  ## ")
                        print("  ##    ####  ####         ###    ##  #  ## ")
                        print("")



    def connection(self):

        self.clientSocket = newSocket(socket(AF_INET, SOCK_STREAM))
        self.clientSocket.connect((self.serverName, self.serverPort))


    def shipment(self, type: str, input):

        self.clientSocket.send(self.Encoder(type, input).encode())


    def catch(self):

        self.buffer = self.clientSocket.recv(1024).decode()


    def close(self):

        self.clientSocket.close()




class arguments():                                      #Clase encargada de interpretarlos argumentos introducidos en el terminal

    ip = "0.0.0.0"
    port = 9001
    name = ""

    nameError: bool
    portError: bool
    ipError: bool

    def __init__(self):
        (opts, args) = getopt.getopt(sys.argv[1:], "n:i:p:", ["name=", "ip=", "port="])
        for o, a in opts:
            if o in ("-n", "--name"):
                self.name = a
            elif o in ("-i", "--ip"):
                self.ip = a
            elif o in ("-p", "--port"):
                self.port = a
        self.nameError = False
        self.portError = False
        self.ipError = False




    def argumentError(self):

        if len(self.name) < 0 and len(self.name) > 100:
           self.nameError = True
        if len(self.ip) == 0:
            self.ipError =True
        else:
            try:
                self.port = int(self.port)
                if not self.port > 0:
                    self.portError = True
            except ValueError:
                self.portError = True




    def argumentRun(self):
        if self.nameError:
            print("Se ha producido un error.")
            print("error_Type:InvalidInput:type=name")
            input("Pulsa enter para continuar.")
            exit(1)
        if self.ipError:
            print("Se ha producido un error.")
            print("error_Type:InvalidInput:type=ip")
            self.ip = "127.0.0.1"
        if self.portError:
            print("Se ha producido un error.")
            print("error_Type:InvalidInput:type=port")
            self.port = 1234
        else:
            print("Argumentos correctos.")
        input("Pulsa enter para continuar.")







########################## E J E C U C I O N #####################################

terminal("clear")


arguments = arguments()

arguments.argumentError()
arguments.argumentRun()
tcpClient = Client(arguments.ip, arguments.port, arguments.name)


try:
    tcpClient.connection()
except:
    print("Se ha producido un error.")
    print("No se pudo conectar con el servidor.")
    input("Pulsa enter para continuar.")
    terminal("clear")
    exit(1)

terminal("clear")

print("")
print("")
print("##   ##    ###     ###   #######   ####   ####        @@   @@   @   @@    @   @@@@   ")
print("# # # #   #   #   #         #     #       #   #       @ @ @ @   @   @ @   @   @   @  ")
print("#  #  #   #####    ###      #      ####   ####        @  @  @   @   @  @  @   @   @  ")
print("#     #   #   #       #     #     #       #  #        @     @   @   @   @ @   @   @  ")
print("#     #   #   #    ###      #      ####   #   #       @     @   @   @    @@   @@@@   ")
print("")
print("                                                                                   ~By Hearts Punk Records")
print("")
print("")
input("Pulsa enter para continuar.")
terminal("clear")

print("")
print("⚙ Opciones de partida ⚙")
print("")
print("1.Crear partida online")
print("")
print("2.Buscar salas")
print("")



tcpClient.shipment("Menu",input())
terminal("clear")
tcpClient.catch()
tcpClient.Decoder()

#################################################################################
match tcpClient.clientType:
    case "Player 1":
        tcpClient.shipment("TurnSelect",input("Introduce el número de turnos:"))
        #wait match
        tcpClient.catch()
        tcpClient.Decoder()
        #wait round 1
        tcpClient.catch()
        tcpClient.Decoder()
        #round start
        tcpClient.catch()
        terminal("clear")
        tcpClient.Decoder()

        #Turn

        #Turnos
        while not tcpClient.GameOver:
            tcpClient.shipment("Turn", input("Introduce una clave de colores:"))
            tcpClient.catch()
            tcpClient.Decoder("Playing")
            sleep(0.4)

        input("Pulsa enter para continuar.")
        terminal("clear")

        #Key player two
        tcpClient.catch()
        tcpClient.Decoder()
        tcpClient.shipment("Key", input("Introduce la clave a adivinar del otro jugador (no escribas nada para hacerla aleatoria): "))

        #KeyACK
        tcpClient.catch()
        tcpClient.Decoder()


        terminal("clear")
        print("Ronda del rival en proceso...")

        #Turno jugador 2
        tcpClient.GameOver = False
        while not tcpClient.GameOver:
            tcpClient.catch()
            tcpClient.Decoder("Reading")
            sleep(0.4)


    ################################################################
    case "Player 2":
        tcpClient.shipment("Games",input("Selecciona la partida deseada:"))



        # Key player one
        tcpClient.catch()
        tcpClient.Decoder()

        tcpClient.shipment("Key", input("Introduce la clave a adivinar del otro jugador(no escribas nada para hacerla aleatoria): "))

        # KeyACK
        tcpClient.catch()
        tcpClient.Decoder()


        terminal("clear")
        print("Ronda del rival en proceso...")
        # Turn player one


        while not tcpClient.GameOver:
            tcpClient.catch()
            tcpClient.Decoder("Reading")
            sleep(0.4)

        print("Round Finished")


        #WAIT ROUND 2
        tcpClient.catch()
        tcpClient.Decoder()

        #Round start
        tcpClient.catch()
        terminal("clear")
        tcpClient.Decoder()


        #Turn player two

        tcpClient.GameOver = False

        while not tcpClient.GameOver:
            tcpClient.shipment("Turn", input("Introduce una clave de colores:"))
            tcpClient.catch()
            tcpClient.Decoder("Playing")
            sleep(0.4)

tcpClient.catch()
tcpClient.Decoder()

input("Pulsa enter para cerrar el juego.")
terminal("clear")
tcpClient.close()

