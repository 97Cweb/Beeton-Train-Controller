class Building:
    def __init__(self, name):
        self.name = name
        self.lights_on = False
        
    def toggle_lights(self):
        self.lights_on = not self.lights_on
        self.update()