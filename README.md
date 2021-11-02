# FTP Server & FTP Client
### Python application allowing a client to upload & download files to & from server
<br>

#### &nbsp;&nbsp;&nbsp;&nbsp;Made by [@acberton](https://github.com/acberton), [@dguido1](https://github.com/dguido1), [@drotter120](https://github.com/drotter120) & [@justinpoblete](https://github.com/justinpoblete)
#### &nbsp;&nbsp;&nbsp;&nbsp;For CPSC 471 - Computer Communication at [***California State University Fullerton***](http://www.fullerton.edu/)<br><br>&nbsp;&nbsp;&nbsp;&nbsp;Spring 21'

<br>

---
<br>

## Table of contents
* [Overview](#overview)  
* [Instructions](#instructions)
* [File Structure](#file-structure)
* [Demo](#demo)
* [Credits](#credits)
***
<br>

## Overview
* This application allows a *client* to connect to an FTP server
* The FTP server will then allow the client to:
    * Upload a file to the server
    * Download an existing file from the server
    * Close the FTP connection and exit program
* SPECIAL NOTE: When running through Tuffix, socket functions that retrieved addresses would be different (127.0.0.1 and 127.0.1.1). This caused connectivity issues and would recommend running on any another OS. 

##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Please read the instructions section below before proceeding.

---

<br>

## Instructions

#### &nbsp;&nbsp;&nbsp; 1. &nbsp; Download this repository and locate the folder on your computer
#### &nbsp;&nbsp;&nbsp; 2. &nbsp; Before proceeding, ensure you have all the following files:
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[`serv.py`](/serv.py) [`cli.py`](/cli.py) [`client-data.txt`](/test.txt) and the [`uploads`](/uploads) subfolder containing [`server-data.txt`](/uploads/server-data.txt)

#### &nbsp;&nbsp;&nbsp; 3. &nbsp; Open two terminals in your OS. One of these servers will be the server, and the other will be the client.


#### &nbsp;&nbsp;&nbsp; 4. &nbsp; In one of your terminals run the [`serv.py`](/serv.py) script using the following command:
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `python3 serv.py <PORT_NUMBER>` 
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The server name will be printed to the terminal. Copy this, you will need it for the next step

#### &nbsp;&nbsp;&nbsp; 5. &nbsp; In the other terminal, run your cli.py script using the following command:
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `python3 cli.py <server_name> <PORT_NUMBER>` 

#### &nbsp;&nbsp;&nbsp; 6. &nbsp; Once both scripts are running, your client terminal will prompt you to enter one of four ftp commands:

##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `ls` - the server will send a string of file names to the client
##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `get <file_name>` - the server will send a file name to the client
##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `put <file_name>` - the server will recieve the specified filename from the client
##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `close` - the server will close the FTP connection after receiving this command from the client

* Once a command is entered, the server will listen for the file name, open the data channel and finally respond accordingly to the command inputted by the client.

* As noted above, when you are ready to close the session, simply type "close" in the ftp prompt of your client terminal.

---

<br>


## File Structure

* CPSC471-ftp-project
   *  [`serv.py`](/serv.py) - Handles server-side communication with FTP connection
   *  [`cli.py`](/cli.py) - Handles client-side communication with FTP connection
   *  [`client-data.txt`](/client-data.txt) - This represents the default client data
   *  [`uploads`](/uploads) - This represents the server directory location
      *  [`server-data.txt`](/uploads/server-data.txt) - This represents the default server data

---

<br>


## Demo


### &nbsp;&nbsp;&nbsp; LS Command 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![ezgif com-optimize](https://github.com/drotter120/CPSC471-ftp-project/blob/master/demo/ls-00.png)
##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; As expected, the server only returns [`server-data.txt`](/uploads/server-data.txt), the default server data

<br>

### &nbsp;&nbsp;&nbsp; PUT Command 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![ezgif com-optimize](https://github.com/drotter120/CPSC471-ftp-project/blob/master/demo/put-00.png)
##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Here we upload [`client-data.txt`](/client-data.txt) to the server
##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; i.e. [`client-data.txt`](/client-data.txt) can now be found in [`uploads`](/uploads)


<br>

### &nbsp;&nbsp;&nbsp; LS Command 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![ezgif com-optimize](https://github.com/drotter120/CPSC471-ftp-project/blob/master/demo/ls-01.png)
##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Now the server returns [`server-data.txt`](/uploads/server-data.txt) and also [`client-data.txt`](/client-data.txt) since we just sent it to the server in the step above

<br>

### &nbsp;&nbsp;&nbsp; GET Command 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![ezgif com-optimize](https://github.com/drotter120/CPSC471-ftp-project/blob/master/demo/get-00.png)
##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Here we request and download [`server-data.txt`](/uploads/server-data.txt) from the server to the clients computer

---
<br>


## Credits
<br>



<br><br>

* Thanks for reading!
* SPECIAL NOTE: When running through Tuffix, socket functions that retrieved addresses would be different (127.0.0.1 and 127.0.1.1). This caused connectivity issues and would recommend running on any another OS. 
<br/><br/>
