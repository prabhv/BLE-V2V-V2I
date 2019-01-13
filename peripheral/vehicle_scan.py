import dbus
import dbus.mainloop.glib

try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject

from bluez_components import *

mainloop = None



##################CHARACTERISTICS##############################################

##################Vehicle-SERVICE#################################################
##This will contain related vehicle information
class VehicleChrc(Characteristic):
    VEHICLE_CHAR_UUID = '12345678-1234-5678-1234-56789abd0001'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.VEHICLE_CHAR_UUID,  
            ['read'],
            service)
        self.value = bytes('VehicleNum,Info..', 'utf-8')

    def ReadValue(self, options):
        return self.value
        

##Vehicle status will hold the faults on vehicle
class VehicleStatus(Characteristic):
    VEHICLE_STATUS_UUID = '12345678-1234-5678-1234-56789abd0002'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
                self, bus, index,
                self.VEHICLE_STATUS_UUID,
                ['read'],
                service)

    def ReadValue(self, options):
        # Return vehicle status as 'faulty' or 'notfaulty'
        if False:               
            return b'fault'
        else:
            return b'nofault'
        
class VehicleService(Service):
    VEHICLE_SVC_UUID = '12345678-1234-5678-1234-56789abd0000'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.VEHICLE_SVC_UUID, True)
        self.add_characteristic(VehicleChrc(bus, 1, self))
        self.add_characteristic(VehicleStatus(bus, 2, self))
        
###############################################################################



class VehicleApplication(Application):
    def __init__(self, bus):  #def __init__(self, bus, display):
        Application.__init__(self, bus)
        self.add_service(VehicleService(bus, 0))


class VehicleAdvertisement(Advertisement):
    def __init__(self, bus, index):
        Advertisement.__init__(self, bus, index, 'peripheral')
        self.add_service_uuid(VehicleService.VEHICLE_SVC_UUID)
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
    app = VehicleApplication(bus)

    # Create advertisement
    test_advertisement = VehicleAdvertisement(bus, 0)

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



