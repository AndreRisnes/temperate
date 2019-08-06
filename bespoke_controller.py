from datetime import datetime, date, timedelta
from matplotlib import pyplot, dates
import math

from devices import *


air = Air()
freezer = Freezer(air)
heater = Heater(air)

previous_error = 0.0
integral = 0.0

wall_temps = []
air_temps = []
frozen = []
heated = []
targets = []
ticks = []
last_air_temp = air.temp

target = k(18)
freezer.room_temp = k(21)

last_freezer_on = -100
last_heater_on = -100

lookahead_ticks = 8
mode_change_ticks = 15


day = datetime(2019, 7, 12, 0, 0, 0)
for t in range(1440):
    freezer.tick()
    heater.tick()

    ticks.append(day + timedelta(minutes=t))

    air_temps.append(c(air.temp))
    wall_temps.append(c(freezer.wall_temp))
    heated.append(2 + heater.is_on())
    frozen.append(freezer.is_on())
    targets.append(c(target))

    freezer.room_temp = k(21) - 5 * math.sin((t / 1440 * math.pi))

    #d_t = last_air_temp - air.temp
    #if abs(d_t) < 0.01:
    #    eta = 0
    #else:
    #    if target below current, and direction down:
    #    if target above current, and direction up:
    #
    #
    #    eta = abs((target - air.temp) / d_t)
    #last_air_temp = air.temp

    #t 18
    # l a t = 18.5
    # at 19
    # 19 - 12 * (0.5)
    if t == 112:
        i = 0

    e_t_1 = air.temp - (lookahead_ticks * (last_air_temp - air.temp))
    last_air_temp = air.temp

    if air.temp > target:  # cooling mode
        heater.off()
        if e_t_1 > target and t - last_heater_on >= mode_change_ticks:
            freezer.on()
            last_freezer_on = t
        else:
            freezer.off()
    else:
        freezer.off()
        if e_t_1 < target - 0.5 and t - last_freezer_on >= mode_change_ticks:
            heater.on()
            last_heater_on = t
        else:
            heater.off()

        #if last_air_temp > air.temp:  # heading down
        #    if e_t_12
    """


        eta = abs((air.temp - target) / (last_air_temp - air.temp))
            if eta > 12:
                freezer.on()
            else:
                freezer.off()
        elif (air.temp - target) > 0.5:
           freezer.on()
    else:
        freezer.off()

    error = target - air.temp
    if error > 0.25:  # heat
        freezer.off()
        if freezer.room_temp < target:  # can't wait for ambient heat
            heater.on()
        else:
            heater.off()
    elif error < -0.25:  # cool
        heater.off()
        if t - last_freezer_toggle > 10:
            if freezer.room_temp > target:  # compensate for ambient
                print(t, eta)
                freezer.on()
            else:
                freezer.off()
                last_freezer_toggle = t
    """
    # print('{:>3} {:4.1f} {:4.1f} {:4.1f} {:4.1f} {:>3} {:>3}'.format(t, c(freezer.room_temp), c(freezer.wall_temp), c(air.temp), eta, freezer.state, heater.state))



fig, ax = pyplot.subplots()

ax.xaxis.set_major_locator(dates.HourLocator())
ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
ax.set_xlim(ticks[0], ticks[-1])

pyplot.plot(ticks, targets)
pyplot.plot(ticks, air_temps)
pyplot.plot(ticks, wall_temps)
pyplot.plot(ticks, frozen)
pyplot.plot(ticks, heated)

pyplot.legend(['target', 'air', 'wall', 'freezer', 'heater'])


fig.set_size_inches(10, 6.0)
fig.autofmt_xdate()

# pyplot.show()


import db

conn = db.connect()

print(1)
for tick in range(len(ticks)):
    db.add_measurement(conn, 'target', targets[tick], ticks[tick] - timedelta(days=1))
print(1)
for tick in range(len(ticks)):
    db.add_measurement(conn, 'air_temp', air_temps[tick], ticks[tick] - timedelta(days=1))
print(1)
for tick in range(900):
    db.add_measurement(conn, 'wall_temp', wall_temps[tick], ticks[tick] - timedelta(days=1))
print(1)
for tick in range(len(ticks)):
    db.add_measurement(conn, 'freezer', frozen[tick], ticks[tick] - timedelta(days=1))
print(1)
for tick in range(500, len(ticks)):
    db.add_measurement(conn, 'heater', heated[tick], ticks[tick] - timedelta(days=1))

print(1)
for tick in range(len(ticks)):
    db.add_measurement(conn, 'target', targets[tick], ticks[tick])
print(1)
for tick in range(len(ticks)):
    db.add_measurement(conn, 'air_temp', air_temps[tick], ticks[tick])
print(1)
for tick in range(900):
    db.add_measurement(conn, 'wall_temp', wall_temps[tick], ticks[tick])
print(1)
for tick in range(len(ticks)):
    db.add_measurement(conn, 'freezer', frozen[tick], ticks[tick])
print(1)
for tick in range(500, len(ticks)):
    db.add_measurement(conn, 'heater', heated[tick], ticks[tick])


conn.close()
