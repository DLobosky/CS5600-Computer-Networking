import sys
from socket import *
from threaded_server import ThreadedServer
import netifaces as ni

server_ip = ni.ifaddresses('eth0')[2][0]['addr']
portMin = 8000
portMax = 9000

def main():

    if (len(sys.argv) == 2 and
        int(sys.argv[1]) >= portMin and
        int(sys.argv[1]) <= portMax):

        # Grabbing desired port number from arguments list
        server_port = int(sys.argv[1])
    else:
		# Prompt for valid port number
		print "  Please enter a port number between %d and %d" % (portMin, portMax)
		server_port = input()

    # Loop until a valid port number is input
    while (server_port < portMin or server_port > portMax):
		print "  Please enter a port number between %d and %d" % (portMin, portMax)
		server_port = input()

    # Outputting IP and port values to be used by clients
    print '\n  Server IP = ' + server_ip

    # Running threaded server with specified port number
    ThreadedServer('', server_port).listen()

    # Notifying of server status
    print '  SERVER: Listening for connections'


if __name__ == '__main__':
    main()
