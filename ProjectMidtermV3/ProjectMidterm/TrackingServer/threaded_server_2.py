from socket import *
import threading
import json
import os.path

class ThreadedServer(threading.Thread):

	"""
		ThreadedServer constructor that initializes all aspects
			of the ThreadedSever class
	"""
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

	"""
		Server side "listen" function definition 
	"""
    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,
                                      args = (client,address)).start()
	"""
		Server side "listenToClient" function definition 
	"""
    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    # Converting received json to dict
                    temp = json.loads(data)

                    if temp['command'] == 'createTracker':
                        createTracker(temp['data'], client)
            	    elif temp['command'] == 'GET':
    	                GET(temp['data'], client)
                    else:
                        response = temp['command']
                        client.send('\n  SERVER: Message received \n    ' +
                                    response + '\n')
                else:
                    raise error('  Client disconnected')
            except:
                client.close()
                print '    Client closed'
                return False
"""
	Server side "createTracker" function definition 
		that creates the TrackerFiles and writes the JSON
		objects to them
"""
def createTracker(data, client):
    client.send("Success")
    file_path = './TrackFiles/' + data['fileName'] + '.track'

    if os.path.isfile(file_path):
        print 'file exists'
        open(file_path, 'w').close()
        with open(file_path, "a+") as f:
            temp = json.dump(data, f, sort_keys=False, indent=4, separators=(',', ': '))
            print data
    else:
        with open(file_path, "a+") as f:
            temp = json.dump(data, f)
"""
	Server side "GET" function definition 
"""
def GET(data, client):

    file_path = './TrackFiles/' + data['fileName'] + '.track'

    if os.path.isfile(file_path):
        with open(file_path) as f:
            client.send(f.read())
    else:
        client.send("SERVER: No such file")
