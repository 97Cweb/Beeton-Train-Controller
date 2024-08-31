def create_devices_table():
    return """
    CREATE TABLE IF NOT EXISTS Devices (
        device_id INTEGER PRIMARY KEY AUTOINCREMENT,
        zigbee_id TEXT UNIQUE NOT NULL,
        device_name TEXT NOT NULL,
        device_type TEXT NOT NULL
    );
    """

def create_trains_table():
    return """
    CREATE TABLE IF NOT EXISTS Trains (
        train_id INTEGER PRIMARY KEY,
        device_id INTEGER NOT NULL,
        FOREIGN KEY (device_id) REFERENCES Devices(device_id)
    );
    """

def create_buildings_table():
    return """
    CREATE TABLE IF NOT EXISTS Buildings (
        building_id INTEGER PRIMARY KEY,
        device_id INTEGER NOT NULL,
        building_type TEXT,
        FOREIGN KEY (device_id) REFERENCES Devices(device_id)
    );
    """

def create_controllers_table():
    return """
    CREATE TABLE IF NOT EXISTS Controllers (
        controller_id INTEGER PRIMARY KEY,
        device_id INTEGER NOT NULL,
        control_type TEXT,
        FOREIGN KEY (device_id) REFERENCES Devices(device_id)
    );
    """

def create_signals_table():
    return """
    CREATE TABLE IF NOT EXISTS Signals (
        signal_id INTEGER PRIMARY KEY,
        device_id INTEGER NOT NULL,
        signal_type TEXT,
        FOREIGN KEY (device_id) REFERENCES Devices(device_id)
    );
    """

def insert_device():
    return """
    INSERT INTO Devices (zigbee_id, device_name, device_type)
    VALUES (?, ?, ?);
    """

def insert_train():
    return """
    INSERT INTO Trains (device_id)
    VALUES (?);
    """

def insert_building():
    return """
    INSERT INTO Buildings (device_id, building_type)
    VALUES (?, ?);
    """

def insert_controller():
    return """
    INSERT INTO Controllers (device_id, control_type)
    VALUES (?, ?);
    """

def insert_signal():
    return """
    INSERT INTO Signals (device_id, signal_type)
    VALUES (?, ?);
    """

def delete_train():
    return """
    DELETE FROM Trains WHERE device_id = ?;
    """

def delete_building():
    return """
    DELETE FROM Buildings WHERE device_id = ?;
    """

def delete_controller():
    return """
    DELETE FROM Controllers WHERE device_id = ?;
    """

def delete_signal():
    return """
    DELETE FROM Signals WHERE device_id = ?;
    """

def delete_device():
    return """
    DELETE FROM Devices WHERE device_id = ? AND device_type = ?;
    """

def get_device_id():
    return """
    SELECT device_id FROM Devices WHERE device_name = ? AND device_type = ?;
    """
