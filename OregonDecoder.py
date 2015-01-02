#!/usr/bin/python
import os
import io
import string
import sys, getopt

def bitstring(bitcount):
    stream=""
    bits=fh.read(bitcount*2)
    if (len(bits)<bitcount*2):
        return ""
    for pos in range(bitcount):
        stream+="%d" % ord(bits[pos*2])
    return stream

def bytestring(reverse):
    bitcount=8
    pos=0
    bits=fh.read(bitcount*2)
    word=0

    if (len(bits)<bitcount*2):
        return 0
    
    for pos in range(bitcount):
        bit=ord(bits[pos*2])
        word=word+(bit<<pos)
    if reverse:
        word=((word&0xF)<<4)+((word&0xF0)>>4)
    return word
       
def convertflags(flag):
    flagstr=""
    negative=""
    if (flag&2)==2:
        negative="-"
        flagstr+="Negative temperature"
    if flagstr!="":
        flagstr+=","
    if (flag&8)==8:
        flagstr+="Battery low"
    return [flagstr,negative]

def checksumV2(inp):
 return ((inp&0xF0)>>4)+(inp&0xF)

#111111111111 01100 1111 1111 111111000000000110111011000000000000000
#111111111111 01100 1101 0010 010010000000000110111011000000000000000

if __name__ == '__main__':
    inputfile = "/tmp/fifo"
    if (len(sys.argv)==2):
	inputfile = sys.argv[1]
    print 'Input file is ', inputfile
    try:
        fh=open(inputfile,"rb")
    except IOError:
        print("Couldn't open file : "+inputfile)
        exit()
    
    bitcounter=0
    init = [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0] #our preamble
    syncV1 = "01100"
    syncV2 = "11110" # Not really a sync, just to identify Version2, still preamble, as it has 16 instead of 12 bits

    for block in iter(lambda: fh.read(1), ""):
        if bitcounter<(11*2):    
            if init[bitcounter]==ord(block):
                bitcounter=bitcounter+1
            else:
                bitcounter=0
        else:
            print("Sync found")
            fh.read(1)
            bitsync=bitstring(5)
            if (syncV1==bitsync):
                v1=bytestring(True)
                temp1=bytestring(True)
                temp2=bytestring(True)
                checksum=bytestring(True)
                if (v1+temp1+temp2 == checksum):
                    #print("%02X%02X%02X" % (v1,temp1,temp2))
                    rolcode=(v1&0xF0)>>4
                    channel=((v1&0xF)/4)+1
                    flag=(temp2&0xF)
                    flaglist=convertflags(flag)
                    negative=flaglist[0]
                    flagstr=flaglist[1]
                    temperature=("%s%d.%01d" % (negative,((((temp2&0xF0)>>4)<<4)+(temp1&0xF)),(temp1&0xF0)>>4))
                    print("Oregon Scientific V1 - Rolling code %01X - Channel %d - Temperature %s C - Flags (%s) - Checksum: %02X ok" % (rolcode,channel,temperature,flagstr,checksum))
                    
            elif ((syncV2==bitsync) and (bitstring(3)=="101")): # Here we check rest of sync
                v1=bytestring(True)
                v2=bytestring(True)
                sensorid=(v1<<8)+v2
                nibble45=bytestring(True)
                nibble67=bytestring(True)
                channel=(nibble45&0xF0)>>4
                rollingcode=((nibble45&0xF)<<4)+((nibble67&0xF0)>>4)
                flag=nibble67&0xF
                flaglist=convertflags(flag)
                negative=flaglist[0]
                flagstr=flaglist[1]
                temperature=""
                valid="- unknown sensor id"
                if (sensorid==0xEC40): # We already know how to handle THR132N
                    temp1=bytestring(True)
                    temp2=bytestring(True)
                    checksum=bytestring(True)
                    checksum=((checksum&0xF)<<4)+((checksum&0xF0)>>4)
                    temperature=("Temperature %s%d.%01d C" % (negative,((((temp2&0xF0)>>4)<<4)+(temp1&0xF)),(temp1&0xF0)>>4))
                    calcchecksum=checksumV2(v1)+checksumV2(v2)+checksumV2(nibble45)+checksumV2(nibble67)+checksumV2(temp1)+checksumV2(temp2)
                    if (calcchecksum==checksum):
                     valid="ok"
                    else:
                     valid="failed"
                else:
                    temperature=("RawData: %02X %02X %02X %02X " % (bytestring(True),bytestring(True),bytestring(True),bytestring(True))) 
                    checksum=0
                #temperature=("%s%d.%01d" % (negative,((((temp2&0xF0)>>4)<<4)+(temp1&0xF)),(temp1&0xF0)>>4))
                print("Oregon Scientific V2 - Sensor Id %04X - Rolling code %01X - Channel %d - %s - Flags (%s) - Checksum: %02X %s" % (sensorid, rollingcode,channel,temperature,flagstr,checksum,valid))
            bitcounter=0

