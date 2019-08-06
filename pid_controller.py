import matplotlib.pyplot as plt
from devices import *

target = k(17.0)

k_p = 5.0
k_i = 0.05
k_d = 0.05

air = Air()
freezer = Freezer(air)
heater = Heater(air)

previous_error = 0.0
integral = 0.0

wall_temps = []
air_temps = []
frozen = []
heated = []

last_air_temp = air.temp

for t in range(400):
    freezer.tick()
    heater.tick()

    #if 100 < t < 150:
    #    freezer.room_temp += 0.2

    air_temps.append(c(air.temp))
    wall_temps.append(c(freezer.wall_temp))
    heated.append(2 + heater.is_on())
    frozen.append(freezer.is_on())

    error = target - air.temp
    integral += k_i * error
    derivative = -k_d * (air.temp - last_air_temp)

    last_air_temp = air.temp

    output = (k_p * error) + integral + derivative

    if (output - target) > 1000:
        freezer.off()
        heater.on()
    elif (output - target) < -10:
        freezer.on()
        heater.off()
    else:
        freezer.off()
        heater.off()

    print('{:>3} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:>3} {:>3}'.format(t, c(freezer.room_temp), c(freezer.wall_temp), c(air.temp), output, freezer.state, heater.state))


plt.axhline(y=c(target), color='gray', linestyle='-')

plt.plot(air_temps)
plt.plot(wall_temps)
plt.plot(frozen)
plt.plot(heated)

plt.legend(['target', 'air', 'wall', 'freezer', 'heater'])

plt.show()



