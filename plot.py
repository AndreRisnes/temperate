from io import BytesIO
from datetime import datetime, timedelta
from collections import defaultdict
from matplotlib import dates
from matplotlib.figure import Figure


def start_and_end(day):
    today = datetime(day.year, day.month, day.day)
    tomorrow = today + timedelta(days=1)
    return today, tomorrow - timedelta(seconds=1)


def group_measurements(measurements):
    groups = defaultdict(list)
    for m in measurements:
        groups[m[1]].append((m[0], m[2]))
    return groups


def plot(day, measurements):
    groups = group_measurements(measurements)

    figure = Figure()
    ax = figure.subplots()
    ax.xaxis.set_major_locator(dates.HourLocator())
    ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
    ax.set_xlim(*start_and_end(day))

    for name, xy in groups.items():
        x, y = list(zip(*xy))
        ax.plot(x, y, label=name)

    ax.legend()

    figure.set_size_inches(11, 7)
    figure.autofmt_xdate()

    buffer = BytesIO()
    figure.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    return buffer

