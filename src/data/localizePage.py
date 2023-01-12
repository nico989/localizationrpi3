from device import Device
from formatPoint import XYZ
from exception import ConnError, HTTPError
from mathOperation import localize, distanceBetweenTwoPoints, truncate
import tkinter as tk  
import tkinter.ttk as ttk
import threading
import numpy
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from collections import defaultdict

class LocalizePage(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self)
        self._controller = controller
        self._controller.rowconfigure(0, weight=1)
        self._controller.columnconfigure(0, weight=1)
        self.grid(sticky='N'+'S'+'W'+'E')
        self._device = Device() 
        self._distances = defaultdict(list)
        self._initialPositions = []
        self._check = True
        self._getInitialPositions()
        self._graph()     
        self._button()
        self._entryArea()
        self._label()
        self._resizable()
        
    def _graph(self):
        self._figure = Figure(figsize=(5,5), dpi=150)
        
        self._canvas = FigureCanvasTkAgg(self._figure, self)       
        self._canvas.draw()

        self._subplot = self._figure.add_subplot(111, projection='3d')
        
        self._toolbarFrame = tk.Frame(self)
        self._toolbarFrame.grid(row=1, column=0, sticky='W')
        self._toolbar = NavigationToolbar2Tk(self._canvas, self._toolbarFrame)
        self._toolbar.update()

    def _button(self):
        self._buttonPane = tk.Frame(self)
        self._buttonPane.grid(row=2, column=0, sticky='W'+'E')

        ttk.Style().configure('TButton', background='#808080')

        self._saveIPButton = ttk.Button(self._buttonPane, text='SAVE IP', takefocus=False, command=lambda: self._saveIP())
        self._saveIPButton.grid(row=0, column=0, padx=10, pady=10, sticky='E')
        self._locMacLabel = tk.StringVar()
        self._locMacLabel.set('GET FIRST POSITION')
        self._locMacButton = ttk.Button(self._buttonPane, textvariable=self._locMacLabel, takefocus=False, command=lambda: self._posThread())
        self._locMacButton.grid(row=0, column=2, padx=10, pady=10)
        self._returnToDevicePageButton = ttk.Button(self._buttonPane, text='GO TO DEVICE PAGE', takefocus=False, command=lambda: self._returnToDevicePage())
        self._returnToDevicePageButton.grid(row=0, column=3, padx=10, pady=10)

    def _entryArea(self):
        self._ipMac = tk.StringVar()
        self._ipMacEntry = ttk.Entry(self._buttonPane, textvariable=self._ipMac)
        self._ipMacEntry.grid(row=0, column=1, pady=10, sticky='W')

    def _label(self):
        self._product = ttk.Label(self._buttonPane, text=u'\u00A9 Product by Vinci Nicolò', font=('Comic Sans MS', 8))
        self._product.grid(row=0, column=4, pady=10, sticky='SE')
        
    def _resizable(self):
        self.rowconfigure(0, weight=50)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        for x in range(5):
            self._buttonPane.columnconfigure(x, weight=1)
    
    def _getInitialPositions(self):
        self._initPointsFile = open('src/data/initialPoints.txt', 'r')
        for line in self._initPointsFile.readlines():
            point = tuple(map(float, line.strip('\r\n').split(',')))
            p = XYZ(point[0], point[1], point[2])
            self._initialPositions.append(p)
    
    def _saveIP(self):
        self._device.setIP(self._ipMacEntry.get())
        self._coordinates.setIP(self._ipMacEntry.get())

    def _returnToDevicePage(self):
        self._saveLabel.set('SAVE IP')
        self._locMacLabel.set('GET FIRST POSITION')
        self._controller.showFrame('DevicePage')

    def _posThread(self):
        if self._check:
            threading.Thread(target= self._getPos, daemon=True).start()
        else:
            tk.messagebox.showerror(title='ERROR', message='Another thread is running')

    def _getPos(self):
        try:
            self._check = False            
            if self._updateLabel():
                devices = self._device.getClientsLastTimeSec(10)
                macAddresses = self._device.filterFields(devices, 'kismet.device.base.macaddr')
                for mac in macAddresses:
                    distance = self._device.calcDistanceAccurateSec(mac, 10)
                    if distance is not None:
                        self._distances[mac].append(distance)
                tk.messagebox.showinfo(title='INFO', message='Get position')
            else:
                allMeanPoint = []
                allResult = []
                for mac in self._distances:
                    result = localize(self._initialPositions[0], self._distances[mac][0], self._initialPositions[1], self._distances[mac][1], self._initialPositions[2], self._distances[mac][2])
                    if result is not None:
                        allMeanPoint.append(result['meanPoint'])  
                        allResult.append(result['points'])         
                self._displayGraphAll(allMeanPoint, allResult)
        except ConnError as conn:
            self._locMacLabel.set('GET FIRST POSITION')
            tk.messagebox.showerror(title='ERROR', message=conn)
        except HTTPError as http:
            self._locMacLabel.set('GET FIRST POSITION')
            tk.messagebox.showerror(title='ERROR', message=http)
        finally:
            self._check = True                                  
       
    def _updateLabel(self):
        if self._locMacLabel.get() == 'GET FIRST POSITION':
            self._locMacLabel.set('GET SECOND POSITION')
            return True
        elif self._locMacLabel.get() == 'GET SECOND POSITION':
            self._locMacLabel.set('GET THIRD POSITION')
            return True
        elif self._locMacLabel.get() == 'GET THIRD POSITION':
            self._locMacLabel.set('CALCULATE POSITION')
            return True
        elif self._locMacLabel.get() == 'CALCULATE POSITION':
            self._locMacLabel.set('GET FIRST POSITION')
            return False

    def _displayGraphAll(self, centerPoint, points):
        # TODO: find a way to clear the graph
        allY = []

        for initial in self._initialPositions:
            allY.append(initial.y)
            scatter1 = self._subplot.scatter(initial.x, initial.y, initial.z, color='blue', marker='o')
        
        for centerPoint in centerPoints:
            allY.append(centerPoint.y)
            scatter2 = self._subplot.scatter(centerPoint.x, centerPoint.y, centerPoint.z, color='green', marker='o')

        for index,mac in enumerate(self._distances):
           self._subplot.text(centerPoint[index].x, centerPoint[index].y, centerPoint[index].z, mac)

        self._subplot.set_xlabel('x axis')
        self._subplot.set_ylabel('y axis')
        self._subplot.set_zlabel('z axis')
        self._subplot.set_ylim(max(allY) + 1, min(allY) - 1) #adjust Y
        self._subplot.xaxis._axinfo['juggled'] = (0,0,0)
        self._subplot.yaxis._axinfo['juggled'] = (1,1,1)
        self._subplot.zaxis._axinfo['juggled'] = (2,2,2)

        self._subplot.legend([scatter1, scatter2], ['Initial points', 'Probable devices'])

        self._canvas.get_tk_widget().grid(row=0, column=0, sticky='N'+'S'+'W'+'E')

        self._initialPositions.clear()     

    def _displayGraph(self, radius, centerPoint, points):
        # TODO: find a way to clear the graph
        allY = []

        for point in points:
            allY.append(point.y)
            scatter1 = self._subplot.scatter(point.x, point.y, point.z, color='red', marker='o')

        for initial in self._initialPositions:
            allY.append(initial.y)
            scatter2 = self._subplot.scatter(initial.x, initial.y, initial.z, color='blue', marker='o')
            self._subplot.plot([initial.x, centerPoint.x], [initial.y, centerPoint.y], [initial.z, centerPoint.z], color='black')
            self._subplot.text(numpy.mean([initial.x, centerPoint.x]), numpy.mean([initial.y, centerPoint.y]), numpy.mean([initial.z, centerPoint.z]), str(truncate(distanceBetweenTwoPoints(initial, centerPoint), 3)))

            scatter3 = self._subplot.scatter(centerPoint.x, centerPoint.y, centerPoint.z, color='green', marker='o')
         
        u = numpy.linspace(0, 2 * numpy.pi, 100)
        v = numpy.linspace(0, numpy.pi, 100)
        x = (radius * numpy.outer(numpy.cos(u), numpy.sin(v))) + centerPoint.x
        y = (radius * numpy.outer(numpy.sin(u), numpy.sin(v))) + centerPoint.y
        z = (radius * numpy.outer(numpy.ones(numpy.size(u)), numpy.cos(v))) + centerPoint.z
        self._subplot.plot_surface(x, y, z, rstride=1, cstride=1, color='lightblue', shade=0, alpha=0.5)      

        self._subplot.set_xlabel('x axis')
        self._subplot.set_ylabel('y axis')
        self._subplot.set_zlabel('z axis')
        self._subplot.set_ylim(max(allY) + 1, min(allY) - 1) #adjust Y
        self._subplot.xaxis._axinfo['juggled'] = (0,0,0)
        self._subplot.yaxis._axinfo['juggled'] = (1,1,1)
        self._subplot.zaxis._axinfo['juggled'] = (2,2,2)

        
        self._subplot.legend([scatter1, scatter2, scatter3], ['Probable points', 'Initial points', 'Center of area: ' + str(centerPoint.x) + ',' + str(centerPoint.y) + ',' + str(centerPoint.z)])

        self._canvas.get_tk_widget().grid(row=0, column=0, sticky='N'+'S'+'W'+'E')

        self._initialPositions.clear()     
