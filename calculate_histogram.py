#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import re


def calculate_histogram(user_id):
    histogram = {}
    with open("mood_data.csv", 'r') as data_file:
        for data_line in data_file.readlines():
            if re.match(r'\d+, \d+, [^,]+, -?\d', data_line):
                uid = int(re.match('(\d+), \d+, ([^,]+), -?\d+', data_line).groups()[0])
                mood = re.match('\d+, \d+, ([^,]+), -?\d+', data_line).groups()[0]
                value = int(re.match('\d+, \d+, ([^,]+), (-?\d+)', data_line).groups()[1])
                if uid == user_id:
                    if mood.lower() in histogram:
                        histogram[mood.lower()] = (histogram[mood.lower()][0] + value, histogram[mood.lower()][1] + 1)
                    else:
                        histogram[mood.lower()] = (value, 1)
    answer = ""
    histogram_view = [(v[0]/v[1], k) for k, v in histogram.items()]
    histogram_view.sort(reverse=True)
    for value, mood in histogram_view:
        answer += mood + ": " + str(value) + " (" + str(histogram[mood.lower()][1]) + ")\n"
    return "```\n" + answer + "```"

if __name__ == "__main__":
    print(calculate_histogram(9700336))
