from socket import *
import os
#import threading
import sys
import json
import time
import netifaces as ni

client_ip = ni.ifaddresses('eth0')[2][0]['addr']
portMin = 8000
portMax = 9000
#threadLock = threading.Lock()

"""
	Client side "create_Tracker" function definition 
"""
def create_tracker(track_sock, filename, description, port):
    file_size = 512
    # Creating dict object with command and tracker data
    message = {"command": "createTracker",
               "data": {"fileName": filename,
                        "fileSize": file_size,
                        "description": description,
                        "md5": "kj1213",
                        "peers": [{"ip": client_ip,
                                   "port": port,
                                   "start": 0,
                                   "end": file_size,
                                   "time": time.time()}]
                        }
                }
    #print message

    # Converting message dict to json string
    message = json.dumps(message, message, sort_keys=False, indent=4, separators=(',', ': '))

    # Sending message to the tracker server
    track_sock.send(message)

    # Checking message receival/return
    print track_sock.recv(1024)
"""
	Client side "update_Tracker" function definition 
"""
def update_tracker(track_sock, filename, port):
    message = {
                "command": "updateTracker",
                "data": {"fileName": filename,
                         "peers": [{
                                    "ip": client_ip,
                                    "start": 5,
                                    "end": 10,
                                    "time": time.time()
                                  }]
                        }
              }

    message = json.dumps(message, message, sort_keys=False, indent=4, separators=(',', ': '))

    track_sock.send(message)

    print track_sock.recv(1024)

"""
	Client side "get_tracker_list" function definition 
"""
def get_tracker_list(track_sock):

    list_file = 'list_file.txt'

    message = {"command": "GET",
               "data": {}
               }

    message = json.dumps(message, message, sort_keys=False, indent=4, separators=(',', ': '))

    track_sock.send(message)
    var = track_sock.recv(1024)
    var = json.loads(var)

    with open(list_file, "w") as f:
        for i in var:
            f.write(i)

"""
	Client side "main" function definition
"""
def main():
    if (len(sys.argv) == 3 and int(sys.argv[2]) >= portMin and int(sys.argv[2]) <= portMax):

        # Grabbing desired port number from arguments list
        server_port = int(sys.argv[2])
        server_ip = sys.argv[1]

    else:
        # Prompt for valid port number
        print "  Please enter a port number between %d and %d" % (portMin, portMax)
        server_port = input()
        print "Please enter the server IP address"
        server_ip = input()

    # Loop until a valid port number is input
    while (server_port < portMin or server_port > portMax):
		print "  Please enter a port number between %d and %d" % (portMin, portMax)
		server_port = input()

    # Creating and connecting socket with tracker server
    tracker_socket = socket(AF_INET, SOCK_STREAM)
    tracker_socket.connect((server_ip, server_port))

    print '  CLIENT: Connection to tracker established'

    while 1:
        get_tracker_list(tracker_socket)
        #update_tracker(tracker_socket, 'fileNAme.txt', 8001)
        #create_tracker(tracker_socket, "fileNAme.txt", 512, 8001)
        # # Sending message to socket
        # print '  CLIENT: Input message'
        # message = raw_input('    ')
        # tracker_socket.send(message)
        #
        # print tracker_socket.recv(1024)

    # Closing socket when finished
    tracker_socket.close()


if __name__ == '__main__':
    main()
