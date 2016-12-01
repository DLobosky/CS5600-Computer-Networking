from socket import *
import threading
import json
import os.path
from pprint import pprint

class ThreadedServer(threading.Thread):
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,
                                      args = (client,address)).start()

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
                        print 'Command was GET'
                        get_tracker_list(client)
                    elif temp['command'] == 'LIST':
                        print 'LIST Test'
                    else:
                        response = temp['command']
                        client.send('SERVER: Invalid Command')
                else:
                    raise error('  Client disconnected')
            except:
                client.close()
                print '    Client closed'
                return False

def createTracker(data, client):
    client.send("SERVER: Creation Success")
    file_path = './TrackFiles/' + data['fileName'] + '.track'

    if os.path.isfile(file_path):
        open(file_path, 'w').close()
        with open(file_path, "a+") as f:
            temp = json.dump(data, f, sort_keys=False, indent=4, separators=(',', ': '))
    else:
        with open(file_path, "a+") as f:
            temp = json.dump(data, f)

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

def get_tracker_list(client):
    filenames = []
    for filename in os.listdir('TrackFiles'):
        filenames.append(filename)
    filenames = json.dumps(filenames, filenames)
    print filenames
    client.send(filenames)
