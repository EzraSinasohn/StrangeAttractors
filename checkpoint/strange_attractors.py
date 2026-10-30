from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import math

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=10, height=5, dpi=4):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111, projection = '3d')
        super().__init__(fig)

class MplCanvas2d(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=10, height=5, dpi=4):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

class MainWindow(QMainWindow):
    main_window = True
    def __init__(self):
        super().__init__()
        
        if self.main_window:
            self.g_type = ''
            self.children = []
        
        self.move(0, 0)
        
        self.graph = []
        
        self.x0 = 0.1
        self.y0 = 0
        self.z0 = 0
        self.N = 100000
        self.dt = 0.001
        
        self.defaults = [10, 28, 8/3, 0.195, 0.95, 0.7, 0.6, 3.5, 0.25, 0.1, 0.2, 0.2, 5.7]
        
        self.setWindowTitle("Strange Attractors")
        self.graph_shown = [[], [], []]
        self.layout_variables = QVBoxLayout()
        self.layout_buttons = QHBoxLayout()
        self.layout_graph = QVBoxLayout()
        
        self.lorenz_button = QRadioButton("Lorenz")
        self.thomas_button = QRadioButton("Thomas")
        self.langford_button = QRadioButton("Langford")
        self.rossler_button = QRadioButton("Rossler")
        
        self.new_window_button = QPushButton('New Window')
        
        if not self.main_window:
            self.compare_values_button = QPushButton('Compare Values')
    
        self.lorenz_button.toggled.connect(self.lorenz_selected)
        self.thomas_button.toggled.connect(self.thomas_selected)
        self.langford_button.toggled.connect(self.langford_selected)
        self.rossler_button.toggled.connect(self.rossler_selected)
            
        self.new_window_button.clicked.connect(self.new_window)
        
        self.sc = MplCanvas(self, width=10, height=8, dpi=100)
        self.sc.setFixedHeight(800)
        self.sc.axes.plot(self.graph_shown[0], self.graph_shown[1], self.graph_shown[2])
        
        self.prandtl = self.defaults[0]
        self.rayleigh = self.defaults[1]
        self.geo = self.defaults[2]
        
        self.tb = self.defaults[3]
        
        self.la = self.defaults[4]
        self.lb = self.defaults[5]
        self.lc = self.defaults[6]
        self.ld = self.defaults[7]
        self.le = self.defaults[8]
        self.lf = self.defaults[9]
        
        self.ra = self.defaults[10]
        self.rb = self.defaults[11]
        self.rc = self.defaults[12]

        self.x0_label = QLabel('x0')
        self.x0_box = QDoubleSpinBox()
        self.x0_box.setValue(self.x0)
        self.x0_box.setDecimals(10)
        
        self.y0_label = QLabel('y0')
        self.y0_box = QDoubleSpinBox()
        self.y0_box.setValue(self.y0)
        self.y0_box.setDecimals(10)
        
        self.z0_label = QLabel('z0')
        self.z0_box = QDoubleSpinBox()
        self.z0_box.setValue(self.z0)
        self.z0_box.setDecimals(10)
        
        if self.main_window:
            self.N_label = QLabel('N')
            self.N_box = QSpinBox()
            self.N_box.setRange(0, 1000000)
            self.N_box.setValue(self.N)
            
            self.dt_label = QLabel('dt')
            self.dt_box = QDoubleSpinBox()
            self.dt_box.setRange(0, 10)
            self.dt_box.setDecimals(10)
            self.dt_box.setValue(self.dt)
            self.dt_box.setSingleStep(0.0000000001)
        
        self.x0_box.setSingleStep(0.0000000001)
        self.y0_box.setSingleStep(0.0000000001)
        self.z0_box.setSingleStep(0.0000000001)
        
        
        self.reset_button = QPushButton('Reset')
        self.reset_button.clicked.connect(self.reset)
        
        self.prandtl_box = QSlider()
        self.rayleigh_box = QSlider()
        self.geo_box = QSlider()
        
        self.prandtl_label = QLabel('Prandtl Constant: ' + str(self.prandtl))
        self.rayleigh_label = QLabel('Rayleigh Constant: ' + str(self.rayleigh))
        self.geo_label = QLabel('Geometrical Constant: ' + str(self.geo))
        
        self.tb_box = QSlider()
        
        self.tb_label = QLabel('b: ' + str(self.tb))
        
        self.la_box = QSlider()
        self.lb_box = QSlider()
        self.lc_box = QSlider()
        self.ld_box = QSlider()
        self.le_box = QSlider()
        self.lf_box = QSlider()
        
        self.la_label = QLabel('a: ' + str(self.la))
        self.lb_label = QLabel('b: ' + str(self.lb))
        self.lc_label = QLabel('c: ' + str(self.lc))
        self.ld_label = QLabel('d: ' + str(self.ld))
        self.le_label = QLabel('e: ' + str(self.le))
        self.lf_label = QLabel('f: ' + str(self.lf))
        
        self.ra_box = QSlider()
        self.rb_box = QSlider()
        self.rc_box = QSlider()
        
        self.ra_label = QLabel('a: ' + str(self.ra))
        self.rb_label = QLabel('b: ' + str(self.rb))
        self.rc_label = QLabel('c: ' + str(self.rc))
        
        
        self.prandtl_box.setRange(0, 30000000)
        self.rayleigh_box.setRange(0, 50000000)
        self.geo_box.setRange(0, 5000000)
        
        self.tb_box.setRange(0, 1000000)
        
        self.la_box.setRange(0, 2000000)
        self.lb_box.setRange(0, 1000000)
        self.lc_box.setRange(0, 1000000)
        self.ld_box.setRange(0, 5000000)
        self.le_box.setRange(0, 1000000)
        self.lf_box.setRange(0, 1000000)
        
        self.ra_box.setRange(0, 1000000)
        self.rb_box.setRange(0, 1000000)
        self.rc_box.setRange(0, 10000000)
        
        self.prandtl_box.setValue(int(1000000*self.defaults[0]))
        self.rayleigh_box.setValue(int(1000000*self.defaults[1]))
        self.geo_box.setValue(int(1000000*self.defaults[2]))
        
        self.tb_box.setValue(int(1000000*self.defaults[3]))
        
        self.la_box.setValue(int(1000000*self.defaults[4]))
        self.lb_box.setValue(int(1000000*self.defaults[5]))
        self.lc_box.setValue(int(1000000*self.defaults[6]))
        self.ld_box.setValue(int(1000000*self.defaults[7]))
        self.le_box.setValue(int(1000000*self.defaults[8]))
        self.lf_box.setValue(int(1000000*self.defaults[9]))
        
        self.ra_box.setValue(int(1000000*self.defaults[10]))
        self.rb_box.setValue(int(1000000*self.defaults[11]))
        self.rc_box.setValue(int(1000000*self.defaults[12]))
        
        self.prandtl_box.setOrientation(Qt.Horizontal)
        self.rayleigh_box.setOrientation(Qt.Horizontal)
        self.geo_box.setOrientation(Qt.Horizontal)
        
        self.tb_box.setOrientation(Qt.Horizontal)
        
        self.la_box.setOrientation(Qt.Horizontal)
        self.lb_box.setOrientation(Qt.Horizontal)
        self.lc_box.setOrientation(Qt.Horizontal)
        self.ld_box.setOrientation(Qt.Horizontal)
        self.le_box.setOrientation(Qt.Horizontal)
        self.lf_box.setOrientation(Qt.Horizontal)
        
        self.ra_box.setOrientation(Qt.Horizontal)
        self.rb_box.setOrientation(Qt.Horizontal)
        self.rc_box.setOrientation(Qt.Horizontal)
        
        self.prandtl_label.setToolTip('The ratio of viscosity to thermal diffusivity, which can be used to estimate the thermal conductivity of gases at high temperatures.')
        self.rayleigh_label.setToolTip("A number associated with a fluid's buoyancy-driven flow, with lower values denoting a more laminar flow and higher values denoting a more turbulent flow.")
        self.geo_label.setToolTip('A constant that prevents the graph from scaling infinitely.')
        
        self.tb_label.setToolTip('')
        
        self.la_label.setToolTip('')
        self.lb_label.setToolTip('')
        self.lc_label.setToolTip('')
        self.ld_label.setToolTip('')
        self.le_label.setToolTip('')
        self.lf_label.setToolTip('')
        
        self.ra_label.setToolTip('')
        self.rb_label.setToolTip('')
        self.rc_label.setToolTip('')
        
        self.x0_box.valueChanged.connect(self.slider_changed(self.x0_box))
        self.y0_box.valueChanged.connect(self.slider_changed(self.y0_box))
        self.z0_box.valueChanged.connect(self.slider_changed(self.z0_box))
        
        if self.main_window:
            self.N_box.valueChanged.connect(self.slider_changed(self.N_box))
            
            self.dt_box.valueChanged.connect(self.slider_changed(self.dt_box))
        
        self.prandtl_box.valueChanged.connect(self.slider_changed(self.prandtl_box))
        self.rayleigh_box.valueChanged.connect(self.slider_changed(self.rayleigh_box))
        self.geo_box.valueChanged.connect(self.slider_changed(self.geo_box))
        self.tb_box.valueChanged.connect(self.slider_changed(self.tb_box))
        self.la_box.valueChanged.connect(self.slider_changed(self.la_box))
        self.lb_box.valueChanged.connect(self.slider_changed(self.lb_box))
        self.lc_box.valueChanged.connect(self.slider_changed(self.lc_box))
        self.ld_box.valueChanged.connect(self.slider_changed(self.ld_box))
        self.le_box.valueChanged.connect(self.slider_changed(self.le_box))
        self.lf_box.valueChanged.connect(self.slider_changed(self.lf_box))
        self.ra_box.valueChanged.connect(self.slider_changed(self.ra_box))
        self.rb_box.valueChanged.connect(self.slider_changed(self.rb_box))
        self.rc_box.valueChanged.connect(self.slider_changed(self.rc_box))
        
        if self.main_window:
            widgets = [
                self.lorenz_button,
                self.thomas_button,
                self.langford_button,
                self.rossler_button,
                self.new_window_button,
            ]
        else:
            widgets = [self.compare_values_button]
        for w in widgets:
            self.layout_buttons.addWidget(w)
        widget = QWidget()
        widget.setLayout(self.layout_variables)
        self.layout_graph.addWidget(self.sc)
        self.layout_buttons.addLayout(self.layout_graph)
        if self.main_window:
            self.typers = [
                self.x0_label,
                self.x0_box,
                self.y0_label,
                self.y0_box,
                self.z0_label,
                self.z0_box,
                self.N_label,
                self.N_box,
                self.dt_label,
                self.dt_box,
                self.prandtl_label,
                self.prandtl_box,
                self.rayleigh_label,
                self.rayleigh_box,
                self.geo_label,
                self.geo_box,
                self.tb_label,
                self.tb_box,
                self.la_label,
                self.la_box,
                self.lb_label,
                self.lb_box,
                self.lc_label,
                self.lc_box,
                self.ld_label,
                self.ld_box,
                self.le_label,
                self.le_box,
                self.lf_label,
                self.lf_box,
                self.ra_label,
                self.ra_box,
                self.rb_label,
                self.rb_box,
                self.rc_label,
                self.rc_box,
                self.reset_button,
            ]
        else:
            self.typers = [
                self.x0_label,
                self.x0_box,
                self.y0_label,
                self.y0_box,
                self.z0_label,
                self.z0_box,
                self.prandtl_label,
                self.prandtl_box,
                self.rayleigh_label,
                self.rayleigh_box,
                self.geo_label,
                self.geo_box,
                self.tb_label,
                self.tb_box,
                self.la_label,
                self.la_box,
                self.lb_label,
                self.lb_box,
                self.lc_label,
                self.lc_box,
                self.ld_label,
                self.ld_box,
                self.le_label,
                self.le_box,
                self.lf_label,
                self.lf_box,
                self.ra_label,
                self.ra_box,
                self.rb_label,
                self.rb_box,
                self.rc_label,
                self.rc_box,
                self.reset_button,
            ]
        self.layout_variables.setSpacing(1)
        for t in self.typers:
            self.layout_variables.addWidget(t)
            if isinstance(t, QLabel) or isinstance(t, QDoubleSpinBox) or isinstance(t, QSpinBox):
                t.setFixedHeight(15)
            elif isinstance(t, QPushButton):
                t.setFixedHeight(20)
            else:
                t.setFixedHeight(5)
            t.hide()
        self.layout_variables.addLayout(self.layout_buttons)
        self.setCentralWidget(widget)



        self.show()
        
        self.not_lorenz = [
            self.tb_box,
            self.la_box,
            self.lb_box,
            self.lc_box,
            self.ld_box,
            self.le_box,
            self.lf_box,
            self.ra_box,
            self.rb_box,
            self.rc_box,
            self.tb_label,
            self.la_label,
            self.lb_label,
            self.lc_label,
            self.ld_label,
            self.le_label,
            self.lf_label,
            self.ra_label,
            self.rb_label,
            self.rc_label, 
        ]
        
        self.not_thomas = [
            self.prandtl_box,
            self.rayleigh_box,
            self.geo_box,
            self.la_box,
            self.lb_box,
            self.lc_box,
            self.ld_box,
            self.le_box,
            self.lf_box,
            self.ra_box,
            self.rb_box,
            self.rc_box,
            self.prandtl_label,
            self.rayleigh_label,
            self.geo_label,
            self.la_label,
            self.lb_label,
            self.lc_label,
            self.ld_label,
            self.le_label,
            self.lf_label,
            self.ra_label,
            self.rb_label,
            self.rc_label,
            
        ]
        
        self.not_langford = [
            self.prandtl_box,
            self.rayleigh_box,
            self.geo_box,
            self.tb_box,
            self.ra_box,
            self.rb_box,
            self.rc_box,
            self.prandtl_label,
            self.rayleigh_label,
            self.geo_label,
            self.tb_label,
            self.ra_label,
            self.rb_label,
            self.rc_label,
        ]
        
        self.not_rossler = [
            self.prandtl_box,
            self.rayleigh_box,
            self.geo_box,
            self.tb_box,
            self.la_box,
            self.lb_box,
            self.lc_box,
            self.ld_box,
            self.le_box,
            self.lf_box,
            self.prandtl_label,
            self.rayleigh_label,
            self.geo_label,
            self.tb_label,
            self.la_label,
            self.lb_label,
            self.lc_label,
            self.ld_label,
            self.le_label,
            self.lf_label,
        ]
    def slider_changed(self, box = 0):
        def slider_changed_nest(check = 0):
            if self.main_window:
                if not box in (self.x0_box, self.y0_box, self.z0_box, self.N_box, self.dt_box):
                    check /= 1000000
            else:
                if not box in (self.x0_box, self.y0_box, self.z0_box):
                    check /= 1000000
            if box is self.x0_box:
                self.x0 = check
            elif box is self.y0_box:
                self.y0 = check
            elif box is self.z0_box:
                self.z0 = check
            elif self.main_window and box is self.N_box:
                self.N = check
                for child in self.children:
                    child.N = check
                    child.slider_changed()()
            elif self.main_window and box is self.dt_box:
                self.dt = check
                for child in self.children:
                    child.dt = check
                    child.slider_changed()()
            elif box is self.prandtl_box:
                self.prandtl = check
                self.prandtl_label.setText('Prandtl Constant: ' + str(self.prandtl))
            elif box is self.rayleigh_box:
                self.rayleigh = check
                self.rayleigh_label.setText('Rayleigh Constant: ' + str(self.rayleigh))
            elif box is self.geo_box:
                self.geo = check
                self.geo_label.setText('Geometric Constant: ' + str(self.geo))
            elif box is self.tb_box:
                self.tb = check
                self.tb_label.setText('b: ' + str(self.tb))
            elif box is self.la_box:
                self.la = check
                self.la_label.setText('a: ' + str(self.la))
            elif box is self.lb_box:
                self.lb = check
                self.lb_label.setText('b: ' + str(self.lb))
            elif box is self.lc_box:
                self.lc = check
                self.lc_label.setText('c: ' + str(self.lc))
            elif box is self.ld_box:
                self.ld = check
                self.ld_label.setText('d: ' + str(self.ld))
            elif box is self.le_box:
                self.le = check
                self.le_label.setText('e: ' + str(self.le))
            elif box is self.lf_box:
                self.lf = check
                self.lf_label.setText('f: ' + str(self.lf))
            elif box is self.ra_box:
                self.ra = check
                self.ra_label.setText('a: ' + str(self.ra))
            elif box is self.rb_box:
                self.rb = check
                self.rb_label.setText('b: ' + str(self.rb))
            elif box is self.rc_box:
                self.rc = check
                self.rc_label.setText('c: ' + str(self.rc))
            self.sc.axes.cla()
            if self.main_window:
                if self.lorenz_button.isChecked():
                    self.type = 'lorenz'
                if self.thomas_button.isChecked():
                    self.type = 'thomas'
                if self.langford_button.isChecked():
                    self.type = 'langford'
                if self.rossler_button.isChecked():
                    self.type = 'rossler'
            
            if self.g_type == 'lorenz':
                self.graph = self.lorenz(self.prandtl, self.rayleigh, self.geo, self.x0, self.y0, self.z0, self.dt, self.N)
                self.sc.axes.plot(self.graph[0], self.graph[1], self.graph[2], c = 'red', linewidth = 0.5)
                self.sc.draw()
            if self.g_type == 'thomas':
                self.graph = self.thomas(self.tb, self.x0, self.y0, self.z0, self.dt, self.N)
                self.sc.axes.plot(self.graph[0], self.graph[1], self.graph[2], c = 'orange', linewidth = 0.5)
                self.sc.draw()
            if self.g_type == 'langford':
                self.graph = self.langford(self.la, self.lb, self.lc, self.ld, self.le, self.lf, self.x0, self.y0, self.z0, self.dt, self.N)
                self.sc.axes.plot(self.graph[0], self.graph[1], self.graph[2], c = 'green', linewidth = 0.5)
                self.sc.draw()
            if self.g_type == 'rossler':
                self.graph = self.rossler(self.ra, self.rb, self.rc, self.x0, self.y0, self.z0, self.dt, self.N)
                self.sc.axes.plot(self.graph[0], self.graph[1], self.graph[2], c = 'blue', linewidth = 0.5)
                self.sc.draw()
                
        return slider_changed_nest
        
    def lorenz_selected(self):
        self.g_type = 'lorenz'
        for i in self.not_lorenz:
            i.hide()
        self.x0_box.show()
        self.x0_label.show()
        self.y0_box.show()
        self.y0_label.show()
        self.z0_box.show()
        self.z0_label.show()
        if self.main_window:
            self.N_label.show()
            self.N_box.show()
            self.dt_label.show()
            self.dt_box.show()
        self.reset_button.show()
        self.prandtl_box.show()
        self.rayleigh_box.show()
        self.geo_box.show()
        self.prandtl_label.show()
        self.rayleigh_label.show()
        self.geo_label.show()
        self.sc.axes.cla()
        self.graph = self.lorenz(self.prandtl, self.rayleigh, self.geo, self.x0, self.y0, self.z0, self.dt, self.N)
        self.sc.axes.plot(self.graph[0], self.graph[1], self.graph[2], c = 'red', linewidth = 0.5)
        self.sc.draw()
        
    
    def thomas_selected(self):
        self.g_type = 'thomas'
        for i in self.not_thomas:
            i.hide()
        self.x0_box.show()
        self.x0_label.show()
        self.y0_box.show()
        self.y0_label.show()
        self.z0_box.show()
        self.z0_label.show()
        if self.main_window:
            self.N_label.show()
            self.N_box.show()
            self.dt_label.show()
            self.dt_box.show()
        self.reset_button.show()
        self.tb_box.show()
        self.tb_label.show()
        self.sc.axes.cla()
        self.graph = self.thomas(self.tb, self.x0, self.y0, self.z0, self.dt, self.N)
        self.sc.axes.plot(self.graph[0], self.graph[1], self.graph[2], c = 'orange', linewidth = 0.5)
        self.sc.draw()
        self.layout_variables.addLayout(self.layout_buttons)
                
    def langford_selected(self):
        self.g_type = 'langford'
        for i in self.not_langford:
            i.hide()
        self.x0_box.show()
        self.x0_label.show()
        self.y0_box.show()
        self.y0_label.show()
        self.z0_box.show()
        self.z0_label.show()
        if self.main_window:
            self.N_label.show()
            self.N_box.show()
            self.dt_label.show()
            self.dt_box.show()
        self.reset_button.show()
        self.la_box.show()
        self.lb_box.show()
        self.lc_box.show()
        self.ld_box.show()
        self.le_box.show()
        self.lf_box.show()
        self.la_label.show()
        self.lb_label.show()
        self.lc_label.show()
        self.ld_label.show()
        self.le_label.show()
        self.lf_label.show()
        self.sc.axes.cla()
        self.graph = self.langford(self.la, self.lb, self.lc, self.ld, self.le, self.lf, self.x0, self.y0, self.z0, self.dt, self.N)
        self.sc.axes.plot(self.graph[0], self.graph[1], self.graph[2], c = 'green', linewidth = 0.5)
        self.sc.draw()
        
    def rossler_selected(self):
        self.g_type = 'rossler'
        for i in self.not_rossler:
            i.hide()
        self.x0_box.show()
        self.x0_label.show()
        self.y0_box.show()
        self.y0_label.show()
        self.z0_box.show()
        self.z0_label.show()
        if self.main_window:
            self.N_label.show()
            self.N_box.show()
            self.dt_label.show()
            self.dt_box.show()
        self.reset_button.show()
        self.ra_box.show()
        self.rb_box.show()
        self.rc_box.show()
        self.ra_label.show()
        self.rb_label.show()
        self.rc_label.show()
        self.sc.axes.cla()
        self.graph = self.rossler(self.ra, self.rb, self.rc, self.x0, self.y0, self.z0, self.dt, self.N)
        self.sc.axes.plot(self.graph[0], self.graph[1], self.graph[2], c = 'blue', linewidth = 0.5)
        self.sc.draw()
    
    def new_window(self):
        if not self.g_type == '':
            self.children.append(SubWindow(self.g_type, self))
        
    def lorenz(self, prandtl, rayleigh, geo, x0, y0, z0, dt, N):
        x = x0
        y = y0
        z = z0
        x_list = [x0]
        y_list = [y0]
        z_list = [z0]
        for i in range(N):
            dx = prandtl*(y-x)
            dy = x*(rayleigh-z)-y
            dz = (x*y)-(geo*z)
            x += dx * dt
            y += dy * dt
            z += dz * dt
            x_list.append(x)
            y_list.append(y)
            z_list.append(z)
        return [x_list, y_list, z_list]

    def thomas(self, b, x0, y0, z0, dt, N):
        x = x0
        y = y0
        z = z0
        x_list = [x0]
        y_list = [y0]
        z_list = [z0]
        for i in range(N):
            dx = np.sin(y) - (b * x)
            dy = np.sin(z) - (b * y)
            dz = np.sin(x) - (b * z)
            x += dx * dt
            y += dy * dt
            z += dz * dt
            x_list.append(x)
            y_list.append(y)
            z_list.append(z)
        return [x_list, y_list, z_list]

    def langford(self, a, b, c, d, e, f, x0, y0, z0, dt, N):
        x = x0
        y = y0
        z = z0
        x_list = [x0]
        y_list = [y0]
        z_list = [z0]
        for i in range(N):
            dx = (z - b) * x - d * y
            dy = d * x + (z - b) * y
            dz = c + a * z - ((z ** 3) / 3) - ((x ** 2) + (y ** 2)) * (1 + e * z) + f * z * (x ** 3)
            x += dx * dt
            y += dy * dt
            z += dz * dt
            x_list.append(x)
            y_list.append(y)
            z_list.append(z)
        return [x_list, y_list, z_list]

    def rossler(self, a, b, c, x0, y0, z0, dt, N):
        x = x0
        y = y0
        z = z0
        x_list = [x0]
        y_list = [y0]
        z_list = [z0]
        for i in range(N):
            dx = -y - z
            dy = x + a * y
            dz = b + z * (x - c)
            x += dx * dt
            y += dy * dt
            z += dz * dt
            x_list.append(x)
            y_list.append(y)
            z_list.append(z)
        return [x_list, y_list, z_list]
    
    def reset(self):
        self.x0_box.setValue(0.1)
        self.y0_box.setValue(0)
        self.z0_box.setValue(0)
        
        if self.main_window:
            self.N_box.setValue(100000)
            self.dt_box.setValue(0.001)
        
        self.prandtl_box.setValue(int(1000000*self.defaults[0]))
        self.rayleigh_box.setValue(int(1000000*self.defaults[1]))
        self.geo_box.setValue(int(1000000*self.defaults[2]))
        
        self.tb_box.setValue(int(1000000*self.defaults[3]))
        
        self.la_box.setValue(int(1000000*self.defaults[4]))
        self.lb_box.setValue(int(1000000*self.defaults[5]))
        self.lc_box.setValue(int(1000000*self.defaults[6]))
        self.ld_box.setValue(int(1000000*self.defaults[7]))
        self.le_box.setValue(int(1000000*self.defaults[8]))
        self.lf_box.setValue(int(1000000*self.defaults[9]))
        
        self.ra_box.setValue(int(1000000*self.defaults[10]))
        self.rb_box.setValue(int(1000000*self.defaults[11]))
        self.rc_box.setValue(int(1000000*self.defaults[12]))

        self.sc.axes.view_init(azim = -60, elev = 30, roll = 0)
        self.sc.draw()
    
    def closeEvent(self, event):
        QApplication.closeAllWindows()
        event.accept()
        
        
class SubWindow(MainWindow):
    main_window = False
    def __init__(self, g_type, parent = None):
        self.g_type = g_type
        self.parent = parent
        self.children = []
        super().__init__()
        if self.g_type == 'lorenz':
            self.lorenz_selected()
        if self.g_type == 'thomas':
            self.thomas_selected()
        if self.g_type == 'langford':
            self.langford_selected()
        if self.g_type == 'rossler':
            self.rossler_selected()
        self.compare_values_button.clicked.connect(self.compare)
    
    def compare(self):
        self.children.append(ComparisonWindow(self, np.array(self.parent.graph), np.array(self.graph), self.N, self.dt))
        self.children[-1].show()
            
class ComparisonWindow(QMainWindow):
    def __init__(self, parent, parent_values, child_values, N, dt):
        super().__init__()
        self.setWindowTitle('Comparison')
        self.parent = parent
        self.N = N
        self.dt = dt
        self.round_decimals = int(abs(math.log(self.dt, 10))) + 1
        
        self.x_diff = child_values[0] - parent_values[0]
        self.y_diff = child_values[1] - parent_values[1]
        self.z_diff = child_values[2] - parent_values[2]
        
        self.diff = np.sqrt(self.x_diff**2 + self.y_diff**2 + self.z_diff**2)      
    
        self.layout = QVBoxLayout()
        self.sc = MplCanvas2d(self, width=10, height=8, dpi=100)
        self.sc.setFixedHeight(800)
        self.sc.axes.plot(np.linspace(0, N * dt, N + 1), self.diff)
        self.sc.axes.set_yscale('log')
        self.sc.draw()
        
        self.time = 0
        self.lyapunov = 0
        
        self.time_label = QLabel(f'Time: {round(self.time * self.dt, self.round_decimals)}')
        self.lyapunov_label = QLabel(f'Lyapunov Exponent: {self.lyapunov}')
        
        self.lyapunov_box = QSlider()
        self.lyapunov_box.setRange(0, N)
        self.lyapunov_box.setValue(0)
        self.lyapunov_box.setOrientation(Qt.Horizontal)
        self.lyapunov_box.valueChanged.connect(self.get_lyapunov)
        
        self.max_lyapunov_button = QPushButton('Max Lyapunov')
        self.max_lyapunov_button.clicked.connect(self.get_max_lyapunov)
        
        widget = QWidget()
        self.layout.addWidget(self.sc)
        self.layout.addWidget(self.time_label)
        self.layout.addWidget(self.lyapunov_label)
        self.layout.addWidget(self.lyapunov_box)
        self.layout.addWidget(self.max_lyapunov_button)
        self.setCentralWidget(widget)
        widget.setLayout(self.layout)
    
    def get_lyapunov(self, time):
        self.time_label.setText(f'Time: {round(time * self.dt, self.round_decimals)}')
        if time == 0:
            self.lyapunov = 0
            self.lyapunov_label.setText(f'Lyapunov Exponent: {self.lyapunov}')
            return
        exponent = math.log(self.diff[time] / self.diff[0])
        self.lyapunov = exponent / (time * self.dt)
        self.lyapunov_label.setText(f'Lyapunov Exponent: {self.lyapunov}')
            
    def get_max_lyapunov(self):
        max_time = 0
        max_lyapunov = 0
        for i in range(1, self.N):
            current_lyapunov = math.log(self.diff[i] / self.diff[0]) / (i * self.dt)
            if current_lyapunov > max_lyapunov:
                max_time = i
                max_lyapunov = current_lyapunov
        self.time_label.setText(f'Time: {round(max_time * self.dt, self.round_decimals)}')
        self.lyapunov = max_lyapunov
        self.lyapunov_label.setText(f'Lyapunov Exponent: {self.lyapunov}')
        
        

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
