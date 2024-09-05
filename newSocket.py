from socket import *
import struct

class newSocket(socket):
    def __init__(self, socket):
        self.__socket = socket

    def connect(self, address):
        self.__socket.connect(address)

    def close(self):
        self.__socket.close()

    def recvall(self, count):
        buf = b''
        while count:
            newbuf = self.__socket.recv(count)
            if not newbuf:
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def send(self, data):
        length = len(data)
        self.__socket.sendall(struct.pack('!I', length))
        self.__socket.sendall(data)

    def recv(self, size):  ##Pequeño cambio para evitar mensajes de error en el servidor
        try:
            import struct
            lengthbuf = self.recvall(4)
            length, = struct.unpack('!I', lengthbuf)
            return self.recvall(length)
        except:
            exit()
