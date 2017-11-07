# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
import time
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


plot_thrust = window.addPlot(0, 0, title="Accelerator")
plot_thrust.setYRange(-100, 100, padding=0)
plot_thrust_curve = plot_thrust.plot(pen="y")


plot_steering = window.addPlot(1, 0, title="Steering wheel angle")
plot_steering.setYRange(-360, 360, padding=0)
plot_steering_curve = plot_steering.plot(pen="y")

try:
####################################################
####################################################
####################################################

	# Main loop
	data_thrust = [0]
	data_steering = [0]
	start = time.time()
	for i in range(0, 100):
		data_thrust.append(max(min(data_thrust[-1] + random.uniform(-10, 10), 100), -100))
		data_steering.append(max(min(data_steering[-1] + random.uniform(-36, 36), 360), -360))

		plot_thrust_curve.setData(y=data_thrust)
		plot_steering_curve.setData(y=data_steering)

		application.processEvents()

		sinceLastFrame = time.time() - start - i * 0.1
		timeToSleep = 0.1 - sinceLastFrame

		if (timeToSleep < 0):
			print("Cant ceep up!")
		else:
			time.sleep(timeToSleep)

	end = time.time()
	print("Done [10SEC; " + str(end-start) +"]")
		
####################################################
####################################################
####################################################
except KeyboardInterrupt:
	print("Aborted.")

application.exec()