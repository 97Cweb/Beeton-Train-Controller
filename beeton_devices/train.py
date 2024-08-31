class Train:
    def __init__(self, name, zigbee_id):
        self.name = name
        self.zigbee_id = zigbee_id
        self.active = False
        self.speed = 0
        self.direction = "FORWARD"
        self.lights_on = False
        self.sound_on = False
        
        
    def set_speed(self, speed):
        if speed < 0:
            self.direction = "REVERSE"
            
        else:
            self.direction = "FORWARD"
            
        self.speed = abs(speed)
        self.update()
        
    def toggle_lights(self):
        self.lights_on = not self.lights_on
        self.update()
    
    def toggle_sound(self):
        self.sound_on = not self.sound_on
        self.update()
    
    def update(self):
        command = {
            "id": self.zigbee_id,
            "speed": self.speed,
            "direction":self.direction,
            "lights": self.lights_on,
            "sound": self.sound_on
            }
    def __str__(self):
        return str({
            "name":			self.name,
            "id": 			self.zigbee_id,
            "speed":		self.speed,
            "direction":	self.direction,
            "lights":		self.lights_on,
            "sound":		self.sound_on
            })
    
    def __repr__(self):
        return self.__str__()
