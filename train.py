

class Train:
    def __init__(self, stat: str, value: int):
        self.stat = stat
        self.value = value
        is_hp_or_mp = stat in ["здоровье", "ману"]
        if is_hp_or_mp:
            value = 1 + int((value - 100) / 10)

        self.duration = 3 + value * 4 + value ** 2
        self.current_time_left = self.duration

    def tick(self):
        self.current_time_left = max(0, self.current_time_left - 1)
    
