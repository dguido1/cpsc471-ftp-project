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
import sys
import os
from os import listdir
from os.path import isfile, join
                                         # *** Initialize Client-side Constants ***
HEADER_SIZE = 10                         # Size of the header message. This chunk of data will be used to store the SIZE of incoming command & data strings
DATA_SIZE = 100                          # Bytes that will be read in from the file the client wishes to upload
                                         # ==>  i.e.  file_data = file_obj.read(DATA_SIZE)
FORMAT = "utf-8"                         # A variable-width character encoding format, used for electronic communication
CMD_RSP_PORT = "12345"                   # Command socket response port
dataPort = 5555

NO_MSG = '0'                             # Server sends to client in the case that the given file parameters will NOT be accepted
OK_MSG = '1'                             # Server sends to client giving go ahead for file upload, having analyzed the file parameters
UP_SUCCESS_MSG = '2'                     # Server sends to clent in the case of a successful upload
UP_FAIL_MSG = '3'                        # Server sends to clent in the case of a failed upload

DATA_ADDR = "localhost"		               # Data socket address
DATA_PORT = 5555			                   # Data socket port

#handles connection errors -- restarts program if y, quits if n
def ErrorHandler():
  rsp = input("Connection has broken, would you like to reconnect? y/n: ").lower()
  if rsp == 'y':
    main()
  elif rsp == 'n':
    exit()
  else:
    ErrorHandler()
  
def sendCommand(socket, data):
  data = "".join(data)
  message = data.encode(FORMAT)
  msg_length = len(message)
  send_length = str(msg_length).encode(FORMAT)
  send_length += b' ' * (HEADER_SIZE - len(send_length))
  socket.send(send_length)
  socket.send(message)

def quitCommand(socket, command):
  data = "close|"+CMD_RSP_PORT                           # Form the put command string
  sendCommand(socket, data)                              # Send quit command
  response = receiveData()
  if response is not None:
    print("Response: " + response)                    # Print the servers response
  else:
    print("Error response. Check server logs.")

def lsCommand(socket, command):
  data = "ls|"+CMD_RSP_PORT                              # Form the put command string
  sendCommand(socket, data)                              # Send ls command
  response = receiveData()
  if response is not None:
    print("Response: " + response)                    # Print the servers response
  else:
    print("Error response. Check server logs.")

def receiveData():
  serverName = socket.gethostbyname(socket.gethostname())
  serverAddress = ("0.0.0.0", int(CMD_RSP_PORT))

  serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    serverSocket.bind(serverAddress)
    serverSocket.listen(5)
    print("\nListening for response on port: " + str(CMD_RSP_PORT))
    msg = None

    clientSocket, address = serverSocket.accept()
    print(f"Response from {address} has been recieved.\n")

    msg_length = clientSocket.recv(HEADER_SIZE).decode(FORMAT)
    if msg_length:
      msg_length = int(msg_length)
      msg = clientSocket.recv(msg_length).decode(FORMAT)

    clientSocket.close()

  #handle any connection problems
  except socket.error as error:
    print("Error: {0}".format(error.strerror))
    ErrorHandler()

  except KeyboardInterrupt:
    print("Response cancelled by client (control + c)")

  return msg

"""
  getCommand (cmd_socket, cmds)
  *****************************
  1. Client sends get command & file_name to server
  2. Server sends response message back to client
  
  *** CASE 01: Server responds with OK ==> recv_msg = OK_MSG = '1' ***
  ********************************************************************
    3. Server sends file SIZE and data to server
    4. Client prepares a new file with <file_name>
    5. Client prepares to receive <file_size> of data
    6. Send file to client
    7. Client => get() & save() file
  
  *** CASE 02: Server responds with NO  ==> recv_msg = NO_MSG = '0' ***
  *********************************************************************
    8. Server sends an error message to client
"""

def getCommand(cmd_socket, cmds):
  file_name = cmds[1]		                                   # The name of the file
  file_exists = os.path.isfile(file_name)                  # Conditional variable determining if the file already exists in directory
  upload_success = False                                   # Conditional variable defining the upload status of the file into the directory

  if not file_exists:                                      # If the file doesn't already exist in directory

    cmd_str = "get|" + CMD_RSP_PORT + "|" + file_name      # Form the get command string
    sendCommand(cmd_socket, cmd_str)                       # Send get command

    recv_msg = receiveData()                               # Receive a message back from the server
   
    if recv_msg == OK_MSG:                                 # If the client receives the OK message from the server
      print("OK message received. The server will now send the size of the file.")

      data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
      data_socket.bind(('', dataPort))                                   # Bind the socket to the port
      data_socket.listen(1)

      recv_serv_file = True

      while recv_serv_file:                                              # Continue to accept file from server until while loop expires
        
        print ("Waiting for (data-socket) connections...")

        cli_data_sock, cli_data_addr = data_socket.accept()              # Accept data socket connection from server until the file upload has concluded
        print("Accepted connection from host: ", cli_data_addr, "\n")

        file_size_buff = ""                                              # String buffer containing the size of the data-file
        file_size_buff = recvAll(cli_data_sock, HEADER_SIZE)             # Receive the first 10 bytes, indicating the size of the respective file to be uploaded
        file_size = int(file_size_buff)                                  # File size converted from String to Int format
        print("The file size is ", file_size)

        file_data = ""                                                   # String buffer containing the actual content of the data-file
        file_data = recvAll(cli_data_sock, file_size)                    # Receive (fileSize) bytes of data, includes the entirety of the file sent from the client
        print ("The file data is: ")
        print (file_data)

        new_file = open(file_name, "w")                                  # Create a file within the client directory (Uses ovrwrite-mode, shouldn't matter w/ our case)
        new_file.write(file_data)                                        # Write the reveived data to the newly created file
        new_file.close()                                                 # Close the new file connection

        cli_data_sock.close()                                            # Close client-side data socket
        upload_success = True                                            # Upload was a success, set upload_success variable to True
        recv_serv_file = False                                           # Finished receiving the server file

      if upload_success:                                                 # If the upload was successful
        print("\nThe server has succesfully sent " + file_name)
      else:
        print("\nThe server failed to send " + file_name)

    else:                                                                # If client did not receive OK message from server
      print("NOT OK message received. The server could not find the requested file.")
  else:                                                                  # If file already exists in directory
    print("Requested file already exists in your directory.")

def recvAll(sock, numBytes):
    recvBuff = ""                                        # The buffer
    tempBuff = ""                                        # The temporary buffer

    while len(recvBuff) < numBytes:

      tempBuff = sock.recv(numBytes).decode(FORMAT)      # Attempt to receive bytes
      if not tempBuff:                                   # The other side has closed the socket
        break

      recvBuff += tempBuff                               # Add the received bytes to the buffer
    return recvBuff

"""
  putCommand (cmd_socket, cmds)
  *****************************
  1. Client sends put command & file_name to server  (Connection 01: Control channel)
  2. Server sends response message back to client,  (Connection 01: Control channel)
      i.e. OK('1') or NO('0')

  *** CASE 01: Server responds with OK ==> recv_msg = OK_MSG = '1' ***
  ********************************************************************
    3. Client sends file SIZE to server (Connection 02: Data channel)
    4. Server prepares a new file with <file_name> 
    5. Server prepares to receive <file size> of data 
    6. Send file to server                (Connection 02: Data channel)
    7. Server => get() & save() file      (Connection 02: Data channel)
      
  *** CASE 02: Server responds with NO  ==> recv_msg = NO_MSG = '0' ***
  *********************************************************************
    8. Client displays an error message to user.
"""
def putCommand(cmd_socket, cmds):

  file_name = cmds[1]			                               # The name of the file
  try:
    file_obj = open(file_name, "r")  	                     # Open the file  
  except OSError:
    print("Could not open or read the file: {0}".format(str(file_name)))
    return None

  bytes_sent = 0		                                   	 # Number of bytes sent
  file_data = None		                                   # The file data

  cmd_str = "put|" + CMD_RSP_PORT + "|" + file_name      # Form the put command string
  sendCommand(cmd_socket, cmd_str)                       # Send put command
      
  recv_msg = receiveData()                               # Receive a message back from the server
  if recv_msg is not None:
    if recv_msg == OK_MSG:                                 # OK msg succesfully received

      print("OK message received. The server is now waiting for the size of the file.")

      data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		  # Create a TCP socket
      data_socket.connect((DATA_ADDR, DATA_PORT))						              # Connect to the server

      while True:			                                                    # Keep sending until all is sent

        file_data = file_obj.read(DATA_SIZE)			                        # Read (DATA_SIZE) bytes of data == 100 bytes

        if file_data:								                                      # Make sure we did not hit EOF
          
          data_size_str = str(len(file_data))		                          # Get the size of the data, convert to string format
          
          while len(data_size_str) < 10:			                            # Prepend 0's to the size string until the size is 10 bytes
            data_size_str = "0" + data_size_str
        
          file_data = data_size_str + file_data		                        # Prepend the size of the data to the file data.
          file_data = "".join(file_data)			                            # Join string before encode
          encd_str = file_data.encode(FORMAT)		                          # Encode full string ==> "<file_size><file_data>"
          bytes_sent = 0								                                  # The number of bytes sent
          
          while len(encd_str) > bytes_sent:
            bytes_sent += data_socket.send(encd_str[bytes_sent:])	        # Send the data

        else:												                                    	# The file has been read. We are done
          break
      print ("Sent ", bytes_sent, " total bytes (Including 10 byte header).")
      print ("Size of data sent: ", bytes_sent - HEADER_SIZE)
    else:
      print("Error receiving response.")

   

    data_socket.close()		                                                                            # Close the socket
    file_obj.close()                                                                                  # Close the file                                                       
             
    up_status_msg = receiveData()                                                                     # Check for any word back from the server regaurding
    if up_status_msg is not None:                                                                      # the status of our file upload:
      if up_status_msg == UP_SUCCESS_MSG:                                                               #   1.) File upload was a success
        print("The server has confirmed " + file_name + " was uploaded successfully.")
      elif up_status_msg == UP_FAIL_MSG:                                                                #   2.) File upload failed
        print("Sorry, the server has reported " + file_name + " failed to upload properly.")
    else:
      print("Error recieving up status response")

  else:
    print("NOT OK message received.\nA file with the same name already resides on the server.\nPlease enter a valid file name.")


def handleClientOperations():

  try:                                                    # Check if args exist
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])

  except IndexError:
    print("Please specify serverName and serverPort. \n python cli.py <servername> <serverport>\n")
    exit()

  serverAddress = (serverName, serverPort)
  clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  try:                                                    # Attempt to connect to socket
    clientSocket.connect(serverAddress)

  except socket.error as error: 
    print("Could not connect to server. Check servername, server port, and that it is running.\n")
    print("Error: {0}".format(error.strerror))
    ErrorHandler()

  acpt_usr_ipt = True
  while acpt_usr_ipt:                                     # Continue as long as accept user input is True

    try:
      print("")
      menu = {"ls": 2, "get": 3, "put": 4, "close": 5}
      commands = input("ftp>")
      commands = commands.split()
      if len(commands) >= 1:
        if commands[0] in menu.keys():

          if menu[commands[0]] == 2:                          # LS
            lsCommand(clientSocket, commands)

          elif menu[commands[0]] == 3:                        # GET
            getCommand(clientSocket, commands)

          elif menu[commands[0]] == 4:                        # PUT
            putCommand(clientSocket, commands)
            
          elif menu[commands[0]] == 5:                        # QUIT
            quitCommand(clientSocket, commands)
            acpt_usr_ipt = False
          else:
            print("Invalid command")
        else:                                                 # ERROR
          print("Invalid command")
    except socket.error as error:
      print("Error: {0}".format(error.strerror))
      ErrorHandler()
  
  print("\nAll client-side connections closed, exiting program.\n")

def main():
  handleClientOperations()

if __name__ == "__main__":
  main()
