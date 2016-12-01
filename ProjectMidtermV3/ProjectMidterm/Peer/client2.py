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

def create_tracker(track_sock, filename, description, port):
    file_size = 512
    # Creating dict object with command and tracker data
    message = {"command": "createTracker",
               "data": {"fileName": filename,
                        "fileSize": file_size,
                        "description": description,
                        "md5": "kj1213",
                        "ip": client_ip,
                        "port": port,
                        "peers": [{"ip": client_ip,
                                   "port": port,
                                   "start": 0,
                                   "end": file_size,
                                   "time": time.time()}]
                        }
                }

    # Converting message dict to json string
    message = json.dumps(message, message)


    # Sending message to the tracker server
    track_sock.send(message)
    print 'sent'
    # Checking message receival/return
    print track_sock.recv(1024)

def GET(track_sock, filename):

    # Creating dict object with command and GET data
    GET = {"command": "GET",
           "data": {"fileName": filename}}

    # Converting GET dict to json string
    GET = json.dumps(GET, GET)

    # Sending GET to the tracker server
    track_sock.send(GET)

    # Checking GET receival/return
    var = track_sock.recv(1024)

    file_path = './Trackers/' + fileName + '.track'
    if os.path.isfile(file_path):
        open(file_path, 'w').close()
        with open(file_path, "a+") as f:
            json.dump(var, f, sort_keys=False, indent=4, separators=(',', ': '))
    else:
        with open(file_path, "a+") as f:
            json.dump(var, f, sort_keys=False, indent=4, separators=(',', ': '))


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
        create_tracker(tracker_socket, "filename.txt", 512, 8001)
        #GET(tracker_socket, 'filename.txt')
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
