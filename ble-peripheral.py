import binascii
import struct
import time
from bluepy.btle import Scanner
from bluepy.btle import Peripheral
from bluepy.btle import Service

scanner = Scanner()
devices = scanner.scan(5.0)
ser_uuid = '12345678-1234-5678-1234-56789abc0010'
value = [0x01, 0x02]

for dev in devices:

    for (adtype, desc, value) in dev.getScanData():

    	if dev.addr == 'B8:27:EB:7C:6E:34' or dev.addr == 'b8:27:eb:7c:6e:34' :
                print "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi)
                print "  %s = %s" % (desc, value)
		p = Peripheral("B8:27:EB:7C:6E:34", "public")
		try:
    			services = p.getServiceByUUID(ser_uuid)
		#	for service in services:
			print "UUID %s and peripheral %s and properties" %  (services.uuid, services.peripheral)
			chrs = services.getCharacteristics()
			for chr in chrs:
				print('UUID :' + str(chr.uuid) + 'read' + repr(chr.read()))
				chr.write(value) 

		finally:
    			p.disconnect()
