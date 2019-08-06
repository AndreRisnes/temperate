import matplotlib.pyplot as plt

from simple_pid import PID

from devices import *

air = Air()
freezer = Freezer(air)
heater = Heater(air)

wall_temps = []
air_temps = []
frozen = []
heated = []

target = k(18)

pid = PID(1, 0.5, 0.5, setpoint=target)

for t in range(400):
    freezer.tick()
    heater.tick()

    air_temps.append(c(air.temp))
    wall_temps.append(c(freezer.wall_temp))
    heated.append(2 + heater.is_on())
    frozen.append(freezer.is_on())

    control = pid(air.temp)

    if control < target:
        freezer.on()
        heater.off()
    else:
        heater.on()
        freezer.off()



plt.axhline(y=c(target), color='gray', linestyle='-')

plt.plot(air_temps)
plt.plot(wall_temps)
plt.plot(frozen)
plt.plot(heated)

plt.legend(['target', 'air', 'wall', 'freezer', 'heater'])
plt.show()
