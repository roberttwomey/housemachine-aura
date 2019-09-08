#!/usr/bin/python
import sys
import socket
import select
import fcntl
import struct
import string, math
import time
import datetime
import codecs
import os

"""
This program:
receives a variety of OSC messages and displays them to screen in a text console

valid addresses:
/amelia
/sensor
/alert
/log - general purpose

rtwomey@ucsd.edu	2019

"""

# check if connected to network through interface:
# http://stackoverflow.com/questions/17434079/python-check-to-see-if-host-is-connected-to-network

doPrint = False
doShow = True
doLog = False


# output
printer = None
logfile = None

# display behaviors
timeToNewline = 3.0
bWroteNewline = False
lastSensorTime = 0.0

# printing behaviors
lastPrintTime = 0.0
quiescentTime = 10.0
bPrintedNewline = False

# logging behaviors
logfileStartTime = 0.0
logfileDuration = 3600.0 # 1 hour

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15]))
    )[20:24])

def OSCString(next):
    """Convert a string into a zero-padded OSC String.
    The length of the resulting string is always a multiple of 4 bytes.
    The string ends with 1 to 4 zero-bytes ('\x00') 
    """
    
    OSCstringLength = math.ceil((len(next)+1) / 4.0) * 4
    return struct.pack(">%ds" % (OSCstringLength), str(next))


def getBinary(address, typetags, message):
        """Returns the binary representation of the message
        """
        binary = OSCString(address)
        binary += OSCString(typetags)
        binary += message
        
        return binary

# def _transmit(self, data):
#         sent = 0
#         while sent < len(data):
#             tmp = self.connection.send(data[sent:])
#             if tmp == 0:
#                 return False
#             sent += tmp
#         return True
        
def sendOSCMsg(msg):
        try:
            binary = getBinary(msg)
            length = len(binary)
            # prepend length of packet before the actual message (big endian)
            len_big_endian = array.array('c', '\0' * 4)
            struct.pack_into(">L", len_big_endian, 0, length)
            len_big_endian = len_big_endian.tostring()
            if _transmit(len_big_endian) and _transmit(binary):
                return True
            return False            
        except socket.error as e:
            if e[0] == errno.EPIPE: # broken pipe
                return False
            raise e

def _readString(data):
    """Reads the next (null-terminated) block of data
    """
    length   = string.find(data,"\0")
    nextData = int(math.ceil((length+1) / 4.0) * 4)
    return (data[0:length], data[nextData:])

def _readBlob(data):
    """Reads the next (numbered) block of data
    """
    
    length   = struct.unpack(">i", data[0:4])[0]
    nextData = int(math.ceil((length) / 4.0) * 4) + 4
    return (data[4:length+4], data[nextData:])

def _readInt(data):
    """Tries to interpret the next 4 bytes of the data
    as a 32-bit integer. """
    
    if(len(data)<4):
        print("Error: too few bytes for int", data, len(data))
        rest = data
        integer = 0
    else:
        integer = struct.unpack(">i", data[0:4])[0]
        rest    = data[4:]

    return (integer, rest)

def _readLong(data):
    """Tries to interpret the next 8 bytes of the data
    as a 64-bit signed integer.
     """

    high, low = struct.unpack(">ll", data[0:8])
    big = (long(high) << 32) + low
    rest = data[8:]
    return (big, rest)

def _readTimeTag(data):
    """Tries to interpret the next 8 bytes of the data
    as a TimeTag.
     """
    high, low = struct.unpack(">ll", data[0:8])
    if (high == 0) and (low <= 1):
        time = 0.0
    else:
        time = int(high) + float(low / 1e9)
    rest = data[8:]
    return (time, rest)

def _readFloat(data):
    """Tries to interpret the next 4 bytes of the data
    as a 32-bit float. 
    """
    
    if(len(data)<4):
        print("Error: too few bytes for float", data, len(data))
        rest = data
        float = 0
    else:
        float = struct.unpack(">f", data[0:4])[0]
        rest  = data[4:]

    return (float, rest)

def decodeOSC(data):
    """Converts a binary OSC message to a Python list. 
    """
    table = {"i":_readInt, "f":_readFloat, "s":_readString, "b":_readBlob}
    decoded = []
    address,  rest = _readString(data)
    if address.startswith(","):
        typetags = address
        address = ""
    else:
        typetags = ""

    if address == "#bundle":
        time, rest = _readTimeTag(rest)
        decoded.append(address)
        decoded.append(time)
        while len(rest)>0:
            length, rest = _readInt(rest)
            decoded.append(decodeOSC(rest[:length]))
            rest = rest[length:]

    elif len(rest)>0:
        if not len(typetags):
            typetags, rest = _readString(rest)
        decoded.append(address)
        decoded.append(typetags)
        if typetags.startswith(","):
            for tag in typetags[1:]:
                value, rest = table[tag](rest)
                decoded.append(value)

    return decoded

def openPrinter():
    global printer
    try:
        printer = open('/dev/usb/lp0', 'w')
    except (IOError):
        print("printer not found, exiting.")
        sock.close()
        exit()

    print("printer opened")
    lastPrintTime = time.time()

def closePrinter():
    global printer
    
    printer.close()
    print("printer closed.")

def openLogfile():
    global logfile, logfileStartTime
    data_path = "/home/pi/housemachine/data/sensors/"
    data_file = time.strftime(data_path+"%Y%m%d_%H%M%S.csv")
    logfile = codecs.open(data_file, "w", encoding="utf-8")
    logfileStartTime = time.time()
    print("opening %s for data logging" % data_file)
    logfile.write('ID; address; value; timestamp;\n')


def closeLogfile():
    global logfile, doPrint, printer
    print("closing logfile")
    logfile.close()

    if doPrint:
        if not printer.closed():
            printer.write('\n')
            printer.flush()


tty = os.open("/dev/tty1", os.O_RDWR)
# clear the tty
os.write(tty, b'\033c')

# get IP for host
# from https://stackoverflow.com/a/166520
# UDP_IP = socket.gethostbyname(socket.gethostname())
UDP_IP = get_ip_address('eth0')  
print("IP for eth0 is:", UDP_IP)
# UDP_IP = "192.168.1.10"
UDP_PORT = 9999

servsock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
servsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servsock.bind((UDP_IP, UDP_PORT))
servsock.setblocking(0)

#bcastAddr = "192.168.1.255"
#bsock = socket.socket(socket.AF_INET, # Internet
#                     socket.SOCK_DGRAM) # UDP
#bsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#bsock.bind((bcastAddr, UDP_PORT))
#bsock.setblocking(0)

print("Listening for UDP messages at",UDP_IP,"port",UDP_PORT)
# print("Listening for Broadcast messages at",bcastAddr,"port",UDP_PORT)

if doPrint:
    openPrinter()

if doLog:
    openLogfile()

lasttarget = ""
# socks = [servsock, bsock]
socks = [servsock]
while True:
    try:
        # listen to multiple sockets
        # from here https://stackoverflow.com/a/15101551
        ready_socks,_,_ = select.select(socks, [], [], 0) 
        
        for sock in ready_socks:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            # data = data.split(',')[0]
            data = decodeOSC(data)
            timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f").rstrip("0")    

            typetags = data.pop(1) # remove type tags
            address = data[0]
            
            # toggle printing
            # if address == "/print":
            #     if data[1] == 1:
            #         doPrint = True
            #         openPrinter()
            #     else:
            #         doPrint = False
            #         closePrinter()

            # # toggle logging
            # if address == "/log":
            #     if data[1] == 1:
            #         if doLog == False:
            #             doLog = True
            #             openLogfile()
            #     else:
            #         doLog = False
            #         closeLogfile()

            if doShow:
                # sys.stdout.write(datastr)
                if time.time() - lastSensorTime > timeToNewline:
                    if not bWroteNewline:
                        os.write(tty, "\n")
                        # print ""
                        sys.stdout.flush()                    
                        bWroteNewline = True

                if len(address)>0:

                    if address.startswith("/amelia"):
                    	os.write(tty, '\x1b[1;37;44m'+data[1] +'\x1b[0m')
                        if(len(data)>2):
                            os.write(tty, " "+" ".join(data[2:]))
                    elif address.startswith("/alert"):
                        os.write(tty, '\x1b[1;41m'+data[1] +'\x1b[0m')
                        if(len(data)>2):
                            os.write(tty, " "+" ".join(data[2:]))
                    elif address.startswith("/sensor"):
                        os.write(tty, '\x1b[1;37;42m'+data[1] +'\x1b[0m')
                        if(len(data)>2):
                            os.write(tty, " "+" ".join(data[2:]))
                    elif address.startswith("/log"):
                        os.write(tty, data[1])
                        if(len(data)>2):
                            os.write(tty, " "+" ".join(data[2:]))
                    elif address.startswith("/clear"):
                        os.write(tty, b'\033c')
                    elif address.startswith("/cicada"):
                        if(len(data)>2):
                            os.write(tty, "                                                            \r\n           88                                88             \r\n           \"\"                                88             \r\n                                             88             \r\n ,adPPYba, 88  ,adPPYba, ,adPPYYba,  ,adPPYb,88 ,adPPYYba,  \r\na8\"     \"\" 88 a8\"     \"\" \"\"     `Y8 a8\"    `Y88 \"\"     `Y8  \r\n8b         88 8b         ,adPPPPP88 8b       88 ,adPPPPP88  \r\n\"8a,   ,aa 88 \"8a,   ,aa 88,    ,88 \"8a,   ,d88 88,    ,88  \r\n `\"Ybbd8\"' 88  `\"Ybbd8\"' `\"8bbdP\"Y8  `\"8bbdP\"Y8 `\"8bbdP\"Y8  \r\n                                                            \r\n     ")
                        else:
                            os.write(tty, "      '-.       ,   ,       .-'\r\n         \\    _.-'\"'-._    /\r\n          \\  (_).---.(_)  /\r\n           '-/         \\-'\r\n             \\__.---.__/\r\n             / .'   '. \\\r\n         ,--(_;.-----.;_)--,\r\n        /   |  \\     /  |   \\\r\n       /   /;'-.'._.'.-';\\   \\\r\n    ,-'   /, \\~ \\-=-/ ~/ ,\\   '-,\r\n         ; ;  |~ '.' ~|  ; ;\r\n         |; '  \\=====/  ; ;|\r\n        /| ; ;_| === |_; ; |\\\r\n       / |  \\_/;= = =;\\_/  | \\\r\n     _/  | ; ;_ \\===/ _; ; |  \\_\r\n    `    |  \\_/ ;\\=/; \\_/  |    `\r\n         | \\_| ; ;|; ; |_/ |\r\n         ;\\_/ ; ;/ \\; ; \\_/;\r\n         ;/, ; ; | | ; ; ,\\;\r\n          ; ; ; /   \\ ; ; ;\r\n          \\; ; ;|   |; ; ;/\r\n           \\; ; /   \\ ; ;/\r\n            \\_.'     '._/\r\n ")
                    else:
                        os.write(tty, address[1:])
                    
                lastSensorTime = time.time()
                bWroteNewline = False

                sys.stdout.flush()

            if doPrint:
                if time.time() - lastPrintTime > quiescentTime:
                    if not bPrintedNewline:
                        printer.write("\n\n")
                        printer.flush()                    
                        bPrintedNewline = True

                printer.write(str(data[0][1:])+" ")
                printer.flush()
                lastPrintTime = time.time()
                bPrintedNewline = False

            
            if doLog:
                # check length of new log file
                if time.time() - logfileStartTime > logfileDuration:
                    print("")
                    print(logfileDuration,"minutes elapsed. starting new log...")
                    closeLogfile()
                    openLogfile()
                    logfileStartTime = time.time()

                # write data
                for d in data:
                    logfile.write(str(d)+";")

                # write timestamp
                logfile.write(str(timestamp)+";")
                logfile.write("\n")

                
    except (KeyboardInterrupt):
        print("exiting...")
        break

servsock.close()
print("server socket closed.")

bsock.close()
print("broadcast socket closed.")

if doLog:
    closeLogfile()

if doPrint:
    closePrinter()

