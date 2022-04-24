import os

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.ticker as mticker

from config import COLOR, TAIL

# CHART_MODE in {'LIVE', 'FULL'}
mode = os.environ.get('CHART_MODE', 'LIVE')


def draw_plot(i):
    def update_ticks(x, pos):
        return int(x + min_x)

    ax.cla()
    ax1.cla()
    ax2.cla()

    avg_color = []
    avg_tail = []
    num_of_females = []
    num_of_males = []

    with open("results.txt", "r") as results:
        lines = results.readlines()
        if mode == 'LIVE':
            lines = lines[-100:]

    min_x = int(lines[0].split(';')[4])

    for line in lines:
        elements = line.split(';')
        avg_color.append(float(elements[0]))
        avg_tail.append(float(elements[1]))
        num_of_females.append(int(elements[2]))
        num_of_males.append(int(elements[3]))

    ax.plot(avg_color)
    ax.scatter(len(avg_color) - 1, avg_color[-1])
    ax.text(len(avg_color) - 1, avg_color[-1] + 2, "{:.2f}".format(avg_color[-1]))
    ax.set_ylim(0, COLOR['max'])
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(update_ticks))
    ax.title.set_text('Average color value among males')
    ax.set(xlabel='Epoch', ylabel='Average color value')

    ax1.plot(avg_tail)
    ax1.scatter(len(avg_tail) - 1, avg_tail[-1])
    ax1.text(len(avg_tail) - 1, avg_tail[-1] + 2, "{:.2f}".format(avg_tail[-1]))
    ax1.set_ylim(0, TAIL['max'])
    ax1.xaxis.set_major_formatter(mticker.FuncFormatter(update_ticks))
    ax1.title.set_text('Average tail value among males')
    ax1.set(xlabel='Epoch', ylabel='Average tail value')

    ax2.plot(num_of_females, label='Number of females')
    ax2.plot(num_of_males, label='Number of males')
    ax2.scatter(len(num_of_females) - 1, num_of_females[-1])
    ax2.scatter(len(num_of_males) - 1, num_of_males[-1])
    ax2.text(len(num_of_females) - 1, num_of_females[-1] + 2, "{}".format(num_of_females[-1]))
    ax2.text(len(num_of_males) - 1, num_of_males[-1] + 2, "{}".format(num_of_males[-1]))
    ax2.legend()
    ax2.set_ylim(0, max(max(num_of_females), max(num_of_males)) + 10)
    ax2.xaxis.set_major_formatter(mticker.FuncFormatter(update_ticks))
    ax2.title.set_text("Number of male and female animals")
    ax2.set(xlabel='Epoch', ylabel='Number of animals')


fig = plt.figure(figsize=(12, 6), facecolor='#DEDEDE')
ax = plt.subplot(221)
ax1 = plt.subplot(222)
ax2 = plt.subplot(223)
ax.set_facecolor('#DEDEDE')
ax1.set_facecolor('#DEDEDE')
ax2.set_facecolor('#DEDEDE')

plt.subplots_adjust(wspace=0.3,
                    hspace=0.46)

ani = FuncAnimation(fig, draw_plot, interval=1000)

plt.show()
