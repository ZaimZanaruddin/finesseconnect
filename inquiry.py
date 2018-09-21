# file: inquiry.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: performs a simple device inquiry followed by a remote name request of
#       each discovered device
# $Id: inquiry.py 401 2006-05-05 19:07:48Z albert $
#
import sys
import bluetooth
import os.path, time

def FileCheck(fn):
    try:
      open(fn, "r")
      return 1
    except IOError:
      print "Error: File does not appear to exist."
      return 0


#Searching for nearby devices
print("performing inquiry...")

nearby_devices = bluetooth.discover_devices(
        duration=8, lookup_names=True, flush_cache=True, lookup_class=False)

print("found %d devices" % len(nearby_devices))
i = 0
for  addr, name in nearby_devices:
    try:
        print("%d:  %s - %s" % (i,addr, name))
    except UnicodeEncodeError:
        print("%d  %s - %s" % (i,addr, name.encode('utf-8', 'replace')))
    i+=1

print("Select a device")
device = input()
print("Selected Device: " + nearby_devices[device][1] + "-" + nearby_devices[device][0])



#Connecting through client
if sys.version < '3':
    input = raw_input
    
sock=bluetooth.BluetoothSocket(bluetooth.L2CAP)
bt_addr=nearby_devices[device][0]
port = 0x1001

print("trying to connect to %s on PSM 0x%X" % (bt_addr, port))

sock.connect((bt_addr, port))

#Checks file on local machine
print("Select a txt file in the same directory to send: ")
filename = input()
if(FileCheck(filename) == 0):
    sys.exit()
    


#Opens file and sends to server
    
timeCheck = time.ctime(os.path.getmtime("test.txt"))

filenm = open(filename, "r")                       
while True:
    if timeCheck != time.ctime(os.path.getmtime("test.txt")):
       
        filenm = open("test.txt", "r")
        time.sleep(2)
        for line in filenm:
            sock.send(line)
            print("It works")
        print("Updated")
        sock.send("done")
        timeCheck = time.ctime(os.path.getmtime(filename))
        
    



print("connected.  type stuff")


sock.close()
