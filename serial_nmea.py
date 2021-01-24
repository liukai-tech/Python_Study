import time
import serial
import pynmea2


#read nmea data in file
def read(filename):
    f = open(filename)
    reader = pynmea2.NMEAStreamReader(f)

    while 1:
        for msg in reader.next():
          print(msg)
          #add parse func by Caesar in 2020/02/07
          msginfo = pynmea2.parse(str(msg),True)#msg should convert to string,use str(msg)
          print(repr(msginfo))#print parse msg info

#read nmea data in serial port
def read_serial(filename):
    com = None
    reader = pynmea2.NMEAStreamReader()

    while 1:

        if com is None:
          try:
            com = serial.Serial(filename, baudrate=115200, timeout=5.0)
          except serial.SerialException:
            print('could not connect to %s' % filename)
            time.sleep(5.0)
            continue

        data = com.read_until()#read data until \n
        #print(data)
        #print(data.decode())#data need convert to str(not orgin b')
        for msg in reader.next(data.decode()):
          print(msg)
          msginfo = pynmea2.parse(str(msg),True)#msg should convert to string,use str(msg)
          print(repr(msginfo))#print parse msg info



#add __main__ by Caesar in 2020/02/18  
if __name__ == '__main__':
#    filename = 'COM70'
#    read_serial(filename)
    filename = 'H:/python study/gps_line.txt'
    read(filename)
