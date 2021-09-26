"""
***********************************************************************
  Project:    Programming Assignment
   School:    California State University, Fullerton
   Course:    CPSC-471
     Term:    Spring 2021
 
  Authors:
           1. Anthony Berton    acberton1@csu.fullerton.edu
           2. David Guido       dguido1@csu.fullerton.edu
           3. David Rotter      drotter120@csu.fullerton.edu
           4. Justin Poblete    jpoblete4@csu.fullerton.edu
***********************************************************************
"""

import socket
import os, sys
import time
from os import listdir
from os.path import isfile, join
                                   # *** Initialize Server-side Constants ***
HEADER_SIZE = 10                   # Size of the header message. This chunk of data will be used to store the SIZE of incoming command & data strings
DATA_SIZE = 100                    # Bytes that will be read in from the file the client wishes to upload
                                   # ==>  i.e.  file_data = file_obj.read(DATA_SIZE)
FORMAT = "utf-8"                   # A variable-width character encoding format, used for electronic communication
#RESPONSE_PORT = "12345"           # Command socket response port
dataPort = 5555										 # Data socket response port

NO_MSG = '0'                       # Server sends to client in the case that the given file parameters will NOT be accepted
OK_MSG = '1'                       # Server sends to client giving go ahead for file upload, having analyzed the file parameters
UP_SUCCESS_MSG = '2'               # Server sends to clent in the case of a successful upload
UP_FAIL_MSG = '3'                  # Server sends to clent in the case of a failed upload

DIR_LOCATION = "uploads"           # This location represents this projects "server" directory.

DATA_ADDR = "localhost"		               # Data socket address
DATA_PORT = 5555			                   # Data socket port

#list files in path
def ls_info():
  filestring = ""
  files = (file for file in os.listdir(DIR_LOCATION) 
         if os.path.isfile(os.path.join(DIR_LOCATION, file)))
  for file in files: 
    filestring += (" " + file)
  return filestring

#respond to command
def sendResponse(serverName, responsePort, data):
  serverAddress = (serverName, int(responsePort))
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  time.sleep(1)
  print("\nSending response to {0} on port: {1}\n".format(str(serverName), str(responsePort)))

  try:
    client.connect(serverAddress)
    message = data.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER_SIZE - len(send_length))
    client.send(send_length)
    client.send(message)
  except socket.error as err:
    print("Could not connect to client for data response. Check servername, server port, and that it is running.\n Error: %s" % err.strerror)
    return None



def  handleServerOperations():

  num_conn = 10                                                      # Number of parallel connections that will be accepted by the server
  serv_name = socket.gethostbyname(socket.gethostname()) 
  serv_port = int(sys.argv[1])
  serv_addr = (serv_name, serv_port)
  print("\nHost: " + socket.gethostname())

  cmd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  cmd_socket.bind(('',serv_port))
  cmd_socket.listen(num_conn)
  open_conn = True              

  while open_conn:                                                    # Continue accepting command socket connections from 
                                                                      # the client until the 'close' command is received
    client, address = cmd_socket.accept()
    print(f"\nConnection from {address} has been established.")
    recv_cli_cmds = True           
                                                                      # Continue accepting and analyzing commands from 
    while recv_cli_cmds:                                              # the client until the 'close' command is received
                                                                      # Recv Command Size: Specifically, receive 10 byte header_SIZE, defining the size of the recently
      msg_length = client.recv(HEADER_SIZE).decode(FORMAT)            #                    received command then decode it from (utf-8) to (string) format

      if msg_length:
        msg_length = int(msg_length)                                  # Convert command size from string to int format
        msg = client.recv(msg_length).decode(FORMAT)                  # Recv Command: Specifically, receive (msg_length) amount of command 
                                                                      #               data then decode it from (utf-8) to (string) format
        msg_split = msg.split("|")
        msg_cmd = msg_split[0]
        response_port = int(msg_split[1])

        print("\n***************************")
        print("* Client Command Received *")
        print("    Command: " + msg_cmd)
        print("Port number: " + msg_split[1])
        print("***************************")

        if msg_cmd == "ls":                                                        # *** LS Command Reveived ***
          sendResponse(str(address[0]), response_port, ls_info())                  # Send response to client with LS info (Information regaurding the client-defined directory)
        
        elif msg_cmd == "get":                                                     # *** GET Command Received ***
          file_name = DIR_LOCATION + "/" + msg_split[2]                            # String contains server directory + client-defined file name
          try:
            file_obj = open(file_name, "r")
            sendResponse(str(address[0]), response_port, OK_MSG)                     # Send OK message to client
            send_serv_file = True

            while send_serv_file:                                                    # Send file to client until while loop expires
                                                      # Open the file

              bytes_sent = 0                                                         # Number of bytes sent
              file_data = None                                                       # The file data

              data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		     # Create a TCP socket
              data_socket.connect((DATA_ADDR, DATA_PORT))						                 # Connect to the client

              print("Now sending the file and size of file to client.\n")
              while True:

                file_data = file_obj.read(DATA_SIZE)                                 # Read (DATA_SIZE) bytes of data == 100 bytes

                if file_data:                                                        # Check for EOF
                  data_size_str = str(len(file_data))                                # Convert the size of data to string format

                  while len(data_size_str) < 10:                                     # Prepend 0's to the size string until the size is 10 bytes
                    data_size_str = "0" + data_size_str
                  
                  file_data = data_size_str + file_data                              # Prepend the size of the data to the file data.
                  file_data = "".join(file_data)                                     # Join string before encode
                  encd_str = file_data.encode(FORMAT)                                # Encode full string ==> "<file_size><file_data>"
                  bytes_sent = 0                                                     # The number of bytes sent

                  while len(encd_str) > bytes_sent:
                    bytes_sent += data_socket.send(encd_str[bytes_sent:])            # Send the data

                else:
                  break                                                              # The file has been sent to client. We are done
              print("Sent ", bytes_sent, " total bytes (Including 10 byte header).")
              print("Size of data sent: ", bytes_sent - HEADER_SIZE)

              data_socket.close()                                                    # Close the socket
              file_obj.close()                                                       # Close the file
              send_serv_file = False                                                 # Sending of file is finished
          except OSError:
            print("Could not open or read the file: {0}".format(str(file_name)))
            sendResponse(str(address[0]), response_port, NO_MSG)                     # Send NO message to client

          

        elif msg_cmd == "put":                                                     # *** PUT Command Reveived ***
          file_name = DIR_LOCATION + "/" + msg_split[2]                            # String contains server directory + client-defined file name
          file_exists = os.path.isfile(file_name)                                  # Conditional var defining if file already exists on server
          upload_success = False                                                   # Conditional var defining the upload status of the clients file

          if not file_exists:                                                      # File does NOT already exist on the server

            data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_socket.bind(('', dataPort))								                  	   # Bind the socket to the port
            data_socket.listen(1)	

            sendResponse(str(address[0]), response_port, OK_MSG)                   # Send OK message as a response to client
            recv_cli_file = True                                              

            while recv_cli_file:					                                         # Continue accepting the clients file data
                                                                                   # until the file upload has concluded
              print ("Waiting for (data-socket) connections...")
                                                                                   # Continue accepting data socket connections from  
              cli_data_sock, cli_data_addr = data_socket.accept()			             # the client until the file upload has concluded
              print ("Accepted connection from client: ", cli_data_addr, "\n")
              
              file_size_buff = ""								                  	                # String buffer containing the size of the data-file 
              file_size_buff = recvAll(cli_data_sock, HEADER_SIZE)	    	          # Receive the first 10 bytes, indicating the size of the respective file to be uploaded
              file_size = int(file_size_buff)					            	                # File size converted from String to Int format
              print ("The file size is ", file_size)
              
              file_data = ""										                                    # String buffer containing the actual content of the data-file
              file_data = recvAll(cli_data_sock, file_size)			                    # Receive (fileSize) bytes of data, includes the entirety of the file sent from the client
              print ("The file data is: ")
              print (file_data)

              new_file = open(file_name, "w")                                      # Create a file within the server directory (Uses ovrwrite-mode, shouldn't matter w/ our case)
              new_file.write(file_data)                                            # Write the reveived data to the newly created file
              new_file.close()                                                     # Close the new file connection

              cli_data_sock.close()	                                               # Close server-side data socket
              upload_success = True                                                # Upload was a success, set upload status conditional var to True
              recv_cli_file = False                                                # Done with this upload, set receive client files conditional var to False
                                                                                   # Let the client know the status of the respective
          if upload_success:                                                       # file being uploaded to the server
            sendResponse(str(address[0]), response_port, UP_SUCCESS_MSG)           #   1.) Sent success response
          else:
            sendResponse(str(address[0]), response_port, UP_FAIL_MSG)              #   2.) Sent fail response

        elif msg_cmd == "close":                                                   # *** CLOSE Command Reveived ***
          sendResponse(str(address[0]), response_port, "Closing connection..")
          recv_cli_cmds = False

    open_conn = False                                                    # Exit most outer while loop

  cmd_socket.close()                                                     # Close the command socket connection
  print("All server-side connections closed, exiting program.\n")
                                                                         # Return to main

def recvAll(sock, numBytes):

	recvBuff = ""	                                      # The buffer
	tmpBuff = ""		                                    # The temporary buffer

	while len(recvBuff) < numBytes:

		tmpBuff =  sock.recv(numBytes).decode(FORMAT)     # Attempt to receive bytes
		if not tmpBuff:										                # The other side has closed the socket
			break
		
		recvBuff += tmpBuff                               # Add the received bytes to the buffer
	return recvBuff
		

if __name__ == "__main__":
  handleServerOperations()
