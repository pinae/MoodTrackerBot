#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md
from datetime import datetime, timedelta


def read_day(user_id, offset=0):
    now = datetime.now()
    day = datetime(year=now.year, month=now.month, day=now.day-offset)
    time_data = []
    values = []
    last_mood_value = 0.0
    with open("mood_data.csv", 'r') as mood_file:
        for line in mood_file.readlines():
            point = line.split(',')
            if len(point) < 3:
                continue
            try:
                if int(point[0].strip()) == user_id:
                    time = datetime.fromtimestamp(float(point[1].strip()))
                    if day < time < day + timedelta(hours=24):
                        if len(point) >= 4:
                            mood_value = float(point[3].strip())
                            last_mood_value = mood_value
                        else:
                            mood_value = last_mood_value
                        time_data.append(time)
                        values.append(mood_value)
            except IndexError:
                continue
    return time_data, values


def plot_day(x, y):
    plt.ylim([-2, 2])
    plt.subplots_adjust(bottom=0.1)
    plt.subplots_adjust(top=0.98)
    plt.subplots_adjust(right=0.98)
    plt.subplots_adjust(left=0.08)
    plt.xticks(rotation=25)
    ax = plt.gca()
    xfmt = md.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(x, y, marker='d')
    return plt


if __name__ == "__main__":
    times, mood_values = read_day(9700336, 5)
    plot_day(times, mood_values).savefig("tmp.png")
