import sqlite3

import beeton_devices.queries as queries
from beeton_devices.train import Train
from beeton_devices.controller import Controller
from beeton_devices.signal import Signal

class BeetonDevices:
    
    def __init__(self):
        self.trains = []
        self.buildings = []
        self.controllers = []
        self.signals = []
        self.setup_db()
        self.setup_zigbee()
  
    def setup_db(self):
        conn = sqlite3.connect('beeton.db')
        c = conn.cursor()

        # Execute queries from the external file using dot notation
        c.execute(queries.create_devices_table())
        c.execute(queries.create_trains_table())
        c.execute(queries.create_buildings_table())
        c.execute(queries.create_controllers_table())
        c.execute(queries.create_signals_table())

        conn.commit()
        conn.close()
        
        # Populate existing devices
        self.populate_existing_trains()
        self.populate_existing_buildings()
        self.populate_existing_controllers()
        self.populate_existing_signals()
        
    def populate_existing_trains(self):
        conn = sqlite3.connect('beeton.db')
        c = conn.cursor()

        # Retrieve all trains from the database
        c.execute('''
            SELECT Devices.device_name, Devices.zigbee_id
            FROM Devices
            INNER JOIN Trains ON Devices.device_id = Trains.device_id
        ''')

        # Fetch all matching rows
        rows = c.fetchall()
        
        # Loop through each row and create Train objects, then append them to the list
        for row in rows:
            device_name, zigbee_id = row
            self.trains.append(Train(device_name, zigbee_id))

        conn.close()

    def populate_existing_buildings(self):
        conn = sqlite3.connect('beeton.db')
        c = conn.cursor()

        # Retrieve all buildings from the database
        c.execute('''
            SELECT Devices.device_name, Devices.zigbee_id
            FROM Devices
            INNER JOIN Buildings ON Devices.device_id = Buildings.device_id
        ''')

        rows = c.fetchall()

        # Loop through each row and create Building objects, then append them to the list
        for row in rows:
            device_name, zigbee_id, building_type = row
            self.buildings.append(Building(device_name, zigbee_id, building_type))

        conn.close()

    def populate_existing_controllers(self):
        conn = sqlite3.connect('beeton.db')
        c = conn.cursor()

        # Retrieve all controllers from the database
        c.execute('''
            SELECT Devices.device_name, Devices.zigbee_id, Controllers.control_type
            FROM Devices
            INNER JOIN Controllers ON Devices.device_id = Controllers.device_id
        ''')

        rows = c.fetchall()

        # Loop through each row and create Controller objects, then append them to the list
        for row in rows:
            device_name, zigbee_id, control_type = row
            self.controllers.append(Controller(device_name, zigbee_id, control_type))

        conn.close()

    def populate_existing_signals(self):
        conn = sqlite3.connect('beeton.db')
        c = conn.cursor()

        # Retrieve all signals from the database
        c.execute('''
            SELECT Devices.device_name, Devices.zigbee_id, Signals.signal_type
            FROM Devices
            INNER JOIN Signals ON Devices.device_id = Signals.device_id
        ''')

        rows = c.fetchall()

        # Loop through each row and create Signal objects, then append them to the list
        for row in rows:
            device_name, zigbee_id, signal_type, signal_state = row
            self.signals.append(Signal(device_name, zigbee_id, signal_type, signal_state))

        conn.close()

    def setup_zigbee(self):
        pass
    
    def append_device(self, zigbee_id, device_name, device_type):
        conn = sqlite3.connect('beeton.db')
        c = conn.cursor()

        # Insert into Devices
        c.execute(queries.insert_device(), (zigbee_id, device_name, device_type))
        device_id = c.lastrowid

        # Insert into specific device type table
        if device_type == 'train':
            c.execute(queries.insert_train(), (device_id,))
            self.trains.append(Train(device_name, zigbee_id))
        elif device_type == 'building':
            building_type = additional_info.get('building_type') if additional_info else None
            c.execute(queries.insert_building(), (device_id, building_type))
            self.buildings.append(Building(device_name, zigbee_id, building_type))
        elif device_type == 'controller':
            control_type = additional_info.get('control_type') if additional_info else None
            c.execute(queries.insert_controller(), (device_id, control_type))
            self.controllers.append(Controller(device_name, zigbee_id, control_type))
        elif device_type == 'signal':
            signal_type = additional_info.get('signal_type') if additional_info else None
            signal_state = additional_info.get('signal_state') if additional_info else None
            c.execute(queries.insert_signal(), (device_id, signal_type, signal_state))
            self.signals.append(Signal(device_name, zigbee_id, signal_type, signal_state))

        conn.commit()
        conn.close()

    def remove_device(self, device_name, device_type):
        conn = sqlite3.connect('beeton.db')
        c = conn.cursor()

        # Get the device ID
        c.execute(queries.get_device_id(), (device_name, device_type))
        device_id = c.fetchone()[0]

        # Delete from specific device type table
        if device_type == 'train':
            c.execute(queries.delete_train(), (device_id,))
            device_list = self.trains
        elif device_type == 'building':
            c.execute(queries.delete_building(), (device_id,))
            device_list = self.buildings
        elif device_type == 'controller':
            c.execute(queries.delete_controller(), (device_id,))
            device_list = self.controllers
        elif device_type == 'signal':
            c.execute(queries.delete_signal(), (device_id,))
            device_list = self.signals

        # Delete from Devices
        c.execute(queries.delete_device(), (device_id, device_type))

        # Remove from the appropriate list
        for device in device_list:
            if device.name == device_name:
                device_list.remove(device)
                break

        conn.commit()
        conn.close()
