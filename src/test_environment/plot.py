import matplotlib.pyplot as plt
import numpy

class Plot:
    def __init__(self, title, xLabel, yLabel):
        self._plt = plt
        self._fig = plt.figure()
        self._ax = self._fig.add_subplot(1, 1, 1)
        self._ax.spines['left'].set_position('zero')
        self._ax.spines['bottom'].set_position('center')
        self._ax.spines['right'].set_color('none')
        self._ax.spines['top'].set_color('none')
        self._plt.xlabel(xLabel)
        self._plt.ylabel(yLabel)
        self._plt.title(title)
    
    def line(self, inf, sup, points, m, q):
        x = numpy.linspace(inf, sup, points)
        y = m*x + q
        self._plt.plot(x, y, color='black')
        self._plt.show()
    
    def points(self, valueX, valueY):
        self._plt.scatter(valueX, valueY, color='green', marker='*', s=30) 
        self._plt.show()

    def pointsAndLine(self, valueX, valueY, inf, sup, points, m, q):
        x = numpy.linspace(inf, sup, points)
        y = m*x + q
        self._plt.plot(x, y, color='black')
        self._plt.scatter(valueX, valueY, color='green', marker='*', s=30) 
        self._plt.show()
  