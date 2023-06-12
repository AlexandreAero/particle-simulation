class particle:
    def __init__(self, material_type, life_time, color):
        self.material_type = material_type
        self.life_time = life_time
        self.color = color
        self.is_dirty = True