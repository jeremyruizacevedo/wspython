import socket
import wspy
import threading
 
class EchoConnection(wspy.Connection):
    def onopen(self):
        print 'Connection opened at %s:%d' % self.sock.getpeername()
 
    def onmessage(self, message):
        print 'Received message "%s"' % message.payload
        #self.send(wspy.TextMessage(message.payload))
        for cliente in clientes:
        	if self != cliente:
        		cliente.send(wspy.TextMessage(message.payload))
 
    def onclose(self, code, reason):
    	clientes.remove(self)
        print 'Connection closed'
 
server = wspy.websocket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('', 9998))
server.listen(5)
 
 
class ClientThread(threading.Thread):
 
    def __init__(self,client):
        threading.Thread.__init__(self)
        self.cliente = client
    def run(self):   
    	self.cliente.receive_forever()
 
threadings=[]
 
 
clientes = []
 
while True:
    client, addr = server.accept()
    #EchoConnection(client).receive_forever()
    cliente = EchoConnection(client)
    clientes.append(cliente)
    hilo = ClientThread(cliente)
    hilo.start()
