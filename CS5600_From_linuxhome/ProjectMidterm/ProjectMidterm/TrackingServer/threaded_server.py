from socket import *
import threading
import json
import os.path
from pprint import pprint

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
	Server side "listen" function definition that creates threads
		for the client that timeout after a set period of time
	"""
    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,
                                      args = (client,address)).start()
	""" 
	Server side "listenToClient" function definition that 
		looks for the command that the client sends
	"""
    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    #print data
                    # Converting received json to dict
                    temp = json.loads(data)
                    #print temp
                    if temp['command'] == 'createTracker':
                        createTracker(temp['data'], client)
                    elif temp['command'] == 'updateTracker':
                        updateTracker(temp['data'], client)
                    elif temp['command'] == 'GET':
                        print 'GET command accepted'
                        GET(temp['data'], client)
                    elif temp['command'] == 'LIST':
                        get_tracker_list(client)
                    else:
                        response = temp['command']
                        client.send('SERVER: Invalid Command')
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
    client.send("SERVER: Creation Success")
    file_path = './TrackFiles/' + data['fileName'] + '.track'

    if os.path.isfile(file_path):
        open(file_path, 'w').close()
        with open(file_path, "a+") as f:
            temp = json.dump(data, f, sort_keys=False, indent=4, separators=(',', ': '))
    else:
        with open(file_path, "a+") as f:
            temp = json.dump(data, f, sort_keys=False, indent=4, separators=(',', ': '))

""" 
Server side "upadteTracker" function definition that sends the	
	the update command and then sends the filename, IP addres,
	start byte, end byte, and timestamp
"""
def updateTracker(data, client):

    file_path = './TrackFiles/' + data['fileName'] + '.track'
    var = ''
    present = False

    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            var = json.load(f)

            for peer in var['peers']:
                if peer['ip'] == data['peers'][0]['ip']:
                    present = True

            if present == False:
                var['peers'].append(data['peers'][0])

        open(file_path, 'w').close()
        with open(file_path, "a+") as f:
            temp = json.dump(var, f, sort_keys=False, indent=4, separators=(',', ': '))

        client.send("SERVER: Update Successful")
    else:
        client.send("SERVER: No Tracker Exists")
""" 
Server side "get_tracker_list" function definition that iterates
	through all tracker files and pulls their filename
"""
def get_tracker_list(client):
    filenames = []
    print 'test'
    for filename in os.listdir('TrackFiles'):
        filenames.append(filename)
    filenames = json.dumps(filenames, filenames)
    print filenames
    client.send(filenames)
""" 
Server side "GET" function definition that searches for a .track
	file that contains the requested filename,pulls that JSON 
	object and then sends it back to the client
"""
def GET(data, client):
    file_path = './TrackFiles/' + data['fileName'] + '.track'

    print 'INSIDE GET'

    if os.path.isfile(file_path):
    	print 'FILE EXISTS'
    	with open(file_path, 'r') as f:
            print 'FILE OPEN'
            temp1 = json.load(f)
            print temp1
            temp1 = json.dumps(temp1, temp1)
            print temp1
    	    # m = hashlib.md5()
    	    # m.update(repr(temp1))
    	    #client.send("REP GET BEGIN")
    	    client.send(temp1)
    	    #client.send("REP GET END " + repr(m.digest()))
    else:
        client.send("fail")
