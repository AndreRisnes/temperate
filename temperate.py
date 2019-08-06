import atexit

from datetime import datetime
from flask import Flask, render_template, send_file

import plot
import db

app = Flask(__name__)
conn = db.connect()


class Graph:
    def __init__(self, date):
        self.date = date


@app.route("/")
def history():
    return render_template('temperate.html', graphs=(Graph('2019-07-12'), Graph('2019-07-11')))


@app.route("/figure/<day>")
def figure(day):
    day = datetime.strptime(day, "%Y-%m-%d").date()
    measurements = db.get_measurements(conn, day)
    return send_file(
        plot.plot(day, measurements),
        mimetype='image/png',
        cache_timeout=-1)


if __name__ == '__main__':
    atexit.register(lambda: conn.close())
    app.run()

