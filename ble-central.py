import dbus
import binascii
import struct
import time

try:
  from gi.repository import GObject
except ImportError:
  import gobject as GObject
import sys

from dbus.mainloop.glib import DBusGMainLoop



from bluepy.btle import Scanner
from bluepy.btle import DefaultDelegate
from bluepy.btle import Peripheral
from bluepy.btle import Service

mainloop = None

GATT_CHRC_IFACE =    'org.bluez.GattCharacteristic1'

def generic_error_cb(error):
    print('D-Bus call failed: ' + str(error))
    mainloop.quit()
    
def hr_msrmt_start_notify_cb():
    print('HR Measurement notifications enabled')

class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        
    def handleNotifications(self, cHandle, data):
        print('Data: ' + str(data))
    


scanner = Scanner()
devices = scanner.scan(5.0)


door_service = '12345678-1234-5678-1234-56789abc1000'
door_request_chrc = '12345678-1234-5678-1234-56789abc1002'
door_status_chrc = '12345678-1234-5678-1234-56789abc1001'

elevator_service = '12345678-1234-5678-1234-56789abc2000'
elevator_status_chrc = '12345678-1234-5678-1234-56789abc2001'
elevator_request_chrc = '12345678-1234-5678-1234-56789abc2002'
elevator_priority_chrc = '12345678-1234-5678-1234-56789abc2004'
elevator_pos_chrc = '12345678-1234-5678-1234-56789abc2003'
elevator_door_chrc = '12345678-1234-5678-1234-56789abc2005'

platform_service = '12345678-1234-5678-1234-56789abc3000'
platform_num_chrc = '12345678-1234-5678-1234-56789abc3001'
platform_status_chrc = '12345678-1234-5678-1234-56789abc3002'
platform_info_chrc = '12345678-1234-5678-1234-56789abc3003'

value = "open"

val = bytes(value, 'utf-8')


for dev in devices:

    for (adtype, desc, value) in dev.getScanData():

        if dev.addr == 'B8:27:EB:7C:6E:34' or dev.addr == 'b8:27:eb:7c:6e:34' :
                p = Peripheral("B8:27:EB:7C:6E:34", "public")
                p.setDelegate(MyDelegate())
                try:
                    services = p.getServiceByUUID(elevator_service)
                    print('UUID ' + str(services.uuid) + ' and peripheral ' + str(services.peripheral))
                    chrs = services.getCharacteristics()
                    for chr in chrs:
                        if True: #str(chr.uuid) == door_request_chrc:
                            print(str(chr.uuid) + ' ')
                            print('done')
                            #chr.write(val)
                            print(chr.read().decode('ASCII'))
                               
                        
                        

                finally:
                    p.disconnect()
                break

