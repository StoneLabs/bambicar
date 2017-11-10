# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
from numpy import asarray
from PIL import Image
import time
import math
import random
import threading
import numpy as np
import pyqtgraph as pg

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)
application = QtGui.QApplication([])

window = pg.GraphicsWindow()
window.resize(1000,600)
window.setWindowTitle('BAMBICAR RECORDER')
layout = pg.GraphicsLayout()
window.addItem(layout)

plot_thrust = layout.addPlot(title="Accelerator", row=0, col=0, colspan=1)
plot_thrust.setYRange(-100, 100, padding=0)
plot_thrust.addItem(pg.InfiniteLine(0, angle=0, pen="w"))
plot_thrust_curve = plot_thrust.plot(pen="y")

plot_speed = layout.addPlot(title="Speed", row=0, col=1, colspan=1)
plot_speed.setYRange(0, 220, padding=0)
plot_speed_curve = plot_speed.plot(pen="y")

plot_steering = layout.addPlot(title="Steering wheel angle", row=1, col=0)
plot_steering.setYRange(-540, 540, padding=0)
plot_steering.showAxis('right')
plot_steering.addItem(pg.InfiniteLine(0, angle=0, pen="w"))
plot_steering_curve = plot_steering.plot(pen="y")

image_wheel = Image.open('wheel.png')
plot_wheel = pg.ImageItem(asarray(image_wheel))
plot_wheelPlt = layout.addPlot(1, 1)
plot_wheelPlt.hideAxis('left')
plot_wheelPlt.hideAxis('bottom')
plot_wheelPlt.addItem(plot_wheel)


data_speed_x = []
data_speed_y = []
data_thrust_x = []
data_thrust_y = []
data_steering_x = []
data_steering_y = []

time_start = time.time()
def addData(thrust, steering, speed):
	time_now = time.time()
	time_diff = time_now - time_start

	data_speed_x.append(time_diff)
	data_thrust_x.append(time_diff)
	data_steering_x.append(time_diff)
	data_speed_y.append(speed)
	data_thrust_y.append(thrust)
	data_steering_y.append(steering)

	plot_speed_curve.setData(data_speed_x[-500:], data_speed_y[-500:])
	plot_thrust_curve.setData(data_thrust_x[-500:], data_thrust_y[-500:])
	plot_steering_curve.setData(data_steering_x[-500:], data_steering_y[-500:])

	plot_wheel.setImage(asarray(image_wheel.rotate(-data_steering_y[-1] - 90)))

	if (len(data_thrust_x) % 10 == 0):
		window.setWindowTitle('BAMBICAR RECORDER [RECORDED ' + str(len(data_thrust_x)) + ' DATASETS]')

	application.processEvents()
	
try:
	addData(0,0,0)
	# Main loop
	for i in range(0, 100000):
		addData(max(min(data_thrust_y[-1] + random.uniform(-5, 5), 100), -100),
				max(min(data_steering_y[-1] + random.uniform(-5, 5), 540), -540),
				max(min(data_speed_y[-1] + random.uniform(-5, 5), 200), 000))
		time.sleep(0.05)


except KeyboardInterrupt:
	print("Aborted.")

application.exec()