import dbus
import dbus.mainloop.glib

try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject

from bluez_components import *

mainloop = None



##################CHARACTERISTICS##############################################

##################DOOR-SERVICE#################################################
##Status can be open value 'open' or 'close' value
class DoorChrc(Characteristic):
    DOOR_UUID = '12345678-1234-5678-1234-56789abc1002'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.DOOR_UUID,  
            ['read', 'write'],
            service)
        self.value = bytes('closed', 'utf-8')

    def ReadValue(self, options):
        print('DoorCharacteristic Read:' + repr(self.value))
        return self.value

    def WriteValue(self, value, options):
        print('DoorCharacteristic Write:' + repr(value))
        self.value = value
        
        
class DoorStatus(Characteristic):
    DOOR_STATUS_UUID = '12345678-1234-5678-1234-56789abc1001'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
                self, bus, index,
                self.DOOR_STATUS_UUID,
                ['read'],
                service)

    def ReadValue(self, options):
        # Return Door status as 'faulty' or 'notfaulty'
        if False:               #door_status == 'fault':
            return b'fault'
        else:
            return b'nofault'
        
class DoorService(Service):
    INFRA_SVC_UUID = '12345678-1234-5678-1234-56789abc1000'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.INFRA_SVC_UUID, True)
        self.add_characteristic(DoorChrc(bus, 1, self))
        self.add_characteristic(DoorStatus(bus, 2, self))
        
##################ELEVATOR-SERVICE#################################################
##Status can be open value 'fault' or 'nofault' value
class ElevatorStatus(Characteristic):
    ELEVATOR_STATUS_UUID = '12345678-1234-5678-1234-56789abc2001'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
                self, bus, index,
                self.ELEVATOR_STATUS_UUID,
                ['read'],
                service)

    def ReadValue(self, options):
        # Return Elevator status as 'faulty' or 'notfaulty'
        if False:               
            return b'fault'
        else:
            return b'nofault'


## Return Current  elevator floor number
class ElevatorCurrentPos(Characteristic):
    ELEVATOR_CURRENT_UUID = '12345678-1234-5678-1234-56789abc2003'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.ELEVATOR_CURRENT_UUID,  
            ['read'],
            service)
        self.value = bytes('00', 'utf-8')

    def ReadValue(self, options):
        return self.value
    
    
## Return Current  elevator door status
class ElevatorDoor(Characteristic):
    ELEVATOR_DOOR_UUID = '12345678-1234-5678-1234-56789abc2005'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.ELEVATOR_DOOR_UUID,  
            ['read'],
            service)
        self.value = bytes('open', 'utf-8')

    def ReadValue(self, options):
        return self.value
    
    

##Request the elevator to required floor

class ElevatorRequest(Characteristic):
    ELEVATOR_REQUEST_UUID = '12345678-1234-5678-1234-56789abc2002'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.ELEVATOR_REQUEST_UUID,  
            ['read', 'write'],
            service)
        self.value = bytes('00', 'utf-8')

    def ReadValue(self, options):
        return self.value

    def WriteValue(self, value, options):
        self.value = value
        ##Call elevator request proc, to execute the commands.
        

##elevator priority request for vehicle to make space in elevator
## '00' for no priority '01' for priority

class ElevatorPriority(Characteristic):
    ELEVATOR_PRIORITY_UUID = '12345678-1234-5678-1234-56789abc2004'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.ELEVATOR_PRIORITY_UUID,  
            ['read', 'write'],
            service)
        self.value = bytes('00', 'utf-8')

    def ReadValue(self, options):
        return self.value

    def WriteValue(self, value, options):
        self.value = value


        
class ElevatorService(Service):
    INFRA_SVC_UUID = '12345678-1234-5678-1234-56789abc2000'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.INFRA_SVC_UUID, True)
        self.add_characteristic(ElevatorCurrentPos(bus, 2, self))
        self.add_characteristic(ElevatorRequest(bus, 3, self))
        self.add_characteristic(ElevatorStatus(bus, 1, self))
        self.add_characteristic(ElevatorPriority(bus, 4, self))        
        self.add_characteristic(ElevatorDoor(bus, 5, self))


##################PLATFORM-SERVICE#################################################

## Return Current  platform number
class PlatformNum(Characteristic):
    PLATFORM_NUM_UUID = '12345678-1234-5678-1234-56789abc3001'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
                self, bus, index,
                self.PLATFORM_NUM_UUID,
                ['read'],
                service)
        self.value = bytes('01', 'utf-8')

    def ReadValue(self, options):
        # Return platform number              
        return value



##Status can be value '00' for platform in use or 'FF' otherwise
class PlatformStatus(Characteristic):
    PLATFORM_STATUS_UUID = '12345678-1234-5678-1234-56789abc3002'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.PLATFORM_STATUS_UUID,  
            ['read'],
            service)
        self.value = bytes('00', 'utf-8')

    def ReadValue(self, options):
        # Return Elevator status as 'faulty' or 'notfaulty'
        if False:               
            return b'fault'
        else:
            return b'nofault'

##Next train on the platform

class PlatformInfo(Characteristic):
    PLATFORM_INFO_UUID = '12345678-1234-5678-1234-56789abc3003'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.PLATFORM_INFO_UUID,  
            ['read'],
            service)
        self.value = bytes('TRAIN-DETAILS', 'utf-8')

    def ReadValue(self, options):
        return self.value
        
        
class PlatformService(Service):
    INFRA_SVC_UUID = '12345678-1234-5678-1234-56789abc3000'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.INFRA_SVC_UUID, True)
        self.add_characteristic(PlatformNum(bus, 1, self))
        self.add_characteristic(PlatformInfo(bus, 3, self))
        self.add_characteristic(PlatformStatus(bus, 2, self))


###############################################################################



class InfraApplication(Application):
    def __init__(self, bus):  #def __init__(self, bus, display):
        Application.__init__(self, bus)
        self.add_service(ElevatorService(bus, 0))


class InfraAdvertisement(Advertisement):
    def __init__(self, bus, index):
        Advertisement.__init__(self, bus, index, 'peripheral')
        self.add_service_uuid(ElevatorService.INFRA_SVC_UUID)
        self.include_tx_power = True


def register_ad_cb():
    """
    Callback if registering advertisement was successful
    """
    print('Advertisement registered')


def register_ad_error_cb(error):
    """
    Callback if registering advertisement failed
    """
    print('Failed to register advertisement: ' + str(error))
    mainloop.quit()


def register_app_cb():
    """
    Callback if registering GATT application was successful
    """
    print('GATT application registered')


def register_app_error_cb(error):
    """
    Callback if registering GATT application failed.
    """
    print('Failed to register application: ' + str(error))
    mainloop.quit()


def main():
    global mainloop
    global display

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    # Get ServiceManager and AdvertisingManager
    service_manager = get_service_manager(bus)
    ad_manager = get_ad_manager(bus)

    # Create gatt services
    app = InfraApplication(bus)

    # Create advertisement
    test_advertisement = InfraAdvertisement(bus, 0)

    mainloop = GObject.MainLoop()

    # Register gatt services
    service_manager.RegisterApplication(app.get_path(), {},
                                        reply_handler=register_app_cb,
                                        error_handler=register_app_error_cb)

    # Register advertisement
    ad_manager.RegisterAdvertisement(test_advertisement.get_path(), {},
                                     reply_handler=register_ad_cb,
                                     error_handler=register_ad_error_cb)

    try:
        mainloop.run()
    except KeyboardInterrupt:
        x = x + 1


if __name__ == '__main__':
    main()


