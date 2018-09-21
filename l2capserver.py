
# file: l2capclient.py
# desc: Demo L2CAP server for pybluez.
# $Id: l2capserver.py 524 2007-08-15 04:04:52Z albert $

import bluetooth
import time
import sys

def list_to_txt(data):
    file_name=open("test.txt", "w")
    for i in range(len(data)-1):
        file_name.write(data[i])
    file_name.close()
    

server_sock=bluetooth.BluetoothSocket( bluetooth.L2CAP )

port = 0x1001

server_sock.bind(("",port))
server_sock.listen(1)

                   
client_sock,address = server_sock.accept()
print("Accepted connection from ",address)

dataList = []
while 1:
    data = client_sock.recv(1024)
    print(data)
    dataList.append(data)
    if not data: break
    print(dataList)
    if data == "done":
        list_to_txt(dataList)
        dataList[:] = []
        
 
client_sock.close()
server_sock.close()
