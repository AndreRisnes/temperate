
class Air:
    def __init__(self):
        self.temp = k(21)


class Device:
    def __init__(self):
        self.state = 'off'
        self.ticks = 0
        self.last_toggle = -20

    def on(self):
        if not self.is_on():
            if self.ticks - self.last_toggle > 20:
                self.state = 'on'
                self.last_toggle = self.ticks

    def off(self):
        self.state = 'off'
        self.last_toggle = self.ticks

    def is_on(self):
        return self.state == 'on'

    def tick(self):
        self.ticks += 1


class Heater(Device):
    def __init__(self, air):
        super().__init__()
        self.air = air
        self.heating_rate = 8.0

    def tick(self):
        super().tick()
        if self.is_on():
            self.air.temp += self.heating_rate


class Freezer(Device):
    def __init__(self, air):
        super().__init__()
        self.air = air
        self.wall_temp = k(23.0)
        self.heat_transfer_coeff = 0.02
        self.air_heat_ratio = 0.05

        self.room_temp = k(23.0)

        self.wall_cooling_rate = 0.2
        self.min_wall_temp = k(-15.0)

    def equlibriate(self):
        self.wall_temp += (self.room_temp - self.wall_temp) * self.heat_transfer_coeff

        self.air.temp += self.temp_change_potential()
        self.wall_temp -= self.temp_change_potential() * self.air_heat_ratio

    def cool(self):
        if self.wall_temp > self.min_wall_temp:
            self.wall_temp -= self.wall_cooling_rate

    def tick(self):
        super().tick()
        self.equlibriate()
        if self.is_on():
            self.cool()

    def temp_change_potential(self):
        d_air_temp = self.wall_temp - self.air.temp
        return self.heat_transfer_coeff * d_air_temp


def c(temp):
    return temp - 273.15


def k(temp):
    return temp + 273.15


if __name__ == '__main__':
    air = Air()
    freezer = Freezer(air)
    heater = Heater(air)
    for t in range(200):
        freezer.tick()
        heater.tick()
        print('{:>3} {:4.1f} {:4.1f} {:4.1f} {:>3} {:>3}'.format(t, c(freezer.room_temp), c(freezer.wall_temp), c(air.temp), freezer.state, heater.state))
        if t == 60:
            freezer.on()
        if t == 179:
            freezer.off()
        if t == 180:
            heater.on()
