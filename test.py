from beeton_devices.beeton_devices import BeetonDevices

if __name__ == "__main__":
    #connect to mysql if exists
    devices = BeetonDevices()
    devices.append_device("123a123","train1","train")
    
    print(devices.trains)
    print(devices.buildings)
    print(devices.signals)
    print(devices.controllers)
