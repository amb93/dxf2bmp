#Copyright (c) 2023, Ahmed Albagdady

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

# Author: Ahmed Albagdady
# Date: March 6, 2023
# github.com/amb93/dxf2bmp
# ahmad.elbaghdadi46@gmail.com

#------------------------------------------------------------------------------------------------------------------------------------------------------

#This code reads a DXF file, extracts the attributes of lines and arcs, and uses them to create a blank image with the correct size. 
#Then it draws the lines and arcs on the blank image and optionally adds text overlay to it. Finally, it displays the image on a Qgraphicsview widget.

#The main steps in this code are:

#Read the DXF file using the ezdxf library.
#Extract the lines and arcs from the DXF modelspace.
#Calculate the bounding box of the lines and arcs to create a blank image with the correct size.
#Draw the lines and arcs on the blank image using the cv2.line() and DrawArc() functions.
#Add text overlay to the image using the cv2.putText() function.
#Display the image on a Qt label widget using the displayImage() function.


from PyQt5 import QtCore, QtGui, QtWidgets
import ezdxf
import numpy as np
import cv2
import math
from PIL import Image
from datetime import date

class Ui_dxf2bmp(object):

    def setupUi(self, dxf2bmp):
        dxf2bmp.setObjectName("dxf2bmp")
        dxf2bmp.resize(1073, 653)
        self.centralwidget = QtWidgets.QWidget(dxf2bmp)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_settings = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_settings.setMinimumSize(QtCore.QSize(200, 0))
        self.groupBox_settings.setMaximumSize(QtCore.QSize(250, 16777215))
        self.groupBox_settings.setObjectName("groupBox_settings")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_settings)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox_export = QtWidgets.QGroupBox(self.groupBox_settings)
        self.groupBox_export.setObjectName("groupBox_export")
        self.groupBox_textOverlay = QtWidgets.QGroupBox(self.groupBox_settings)
        self.groupBox_textOverlay.setObjectName("groupBox_textOverlay")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_export)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_textOverlay)
        self.gridLayout_7.setObjectName("gridLayout_7")        
        self.label_export_path = QtWidgets.QLabel(self.groupBox_export)
        self.label_export_path.setObjectName("label_export_path")
        self.gridLayout_6.addWidget(self.label_export_path, 1, 0, 1, 1)
        self.lineEdit_export_path = QtWidgets.QLineEdit(self.groupBox_export)
        self.lineEdit_export_path.setEnabled(False)
        self.lineEdit_export_path.setObjectName("lineEdit_export_path")
        self.gridLayout_6.addWidget(self.lineEdit_export_path, 1, 2, 1, 1)
        self.toolButton_export_path = QtWidgets.QToolButton(self.groupBox_export)
        self.toolButton_export_path.setEnabled(False)
        self.toolButton_export_path.setObjectName("toolButton_export_path")
        self.gridLayout_6.addWidget(self.toolButton_export_path, 1, 3, 1, 1)
        self.pushButton_export = QtWidgets.QPushButton(self.groupBox_export)
        self.pushButton_export.setObjectName("pushButton_export")
        self.gridLayout_6.addWidget(self.pushButton_export, 2, 2, 1, 1)
        self.checkBox_path = QtWidgets.QCheckBox(self.groupBox_export)
        self.checkBox_path.setChecked(True)
        self.checkBox_path.setObjectName("checkBox_path")
        self.gridLayout_6.addWidget(self.checkBox_path, 0, 2, 1, 2)
        self.gridLayout_2.addWidget(self.groupBox_textOverlay, 2, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_export, 3, 0, 1, 1)
        self.groupBox_parameters = QtWidgets.QGroupBox(self.groupBox_settings)
        self.groupBox_parameters.setObjectName("groupBox_parameters")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_parameters)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.spinBox_drop_spacing = QtWidgets.QSpinBox(self.groupBox_parameters)
        self.spinBox_drop_spacing.setMinimum(5)
        self.spinBox_drop_spacing.setMaximum(255)
        self.spinBox_drop_spacing.setSingleStep(5)
        self.spinBox_drop_spacing.setProperty("value", 30)
        self.spinBox_drop_spacing.setObjectName("spinBox_drop_spacing")
        self.gridLayout_4.addWidget(self.spinBox_drop_spacing, 3, 3, 1, 1)
        self.label_sabre_angle = QtWidgets.QLabel(self.groupBox_parameters)
        self.label_sabre_angle.setObjectName("label_sabre_angle")
        self.gridLayout_4.addWidget(self.label_sabre_angle, 5, 1, 1, 1)
        self.label_margin = QtWidgets.QLabel(self.groupBox_parameters)
        self.label_margin.setObjectName("label_margin")
        self.gridLayout_4.addWidget(self.label_margin, 2, 1, 1, 1)
        self.comboBox_floodfill_color = QtWidgets.QComboBox(self.groupBox_parameters)
        self.comboBox_floodfill_color.setObjectName("comboBox_floodfill_color")
        self.comboBox_floodfill_color.addItem("")
        self.comboBox_floodfill_color.addItem("")
        self.gridLayout_4.addWidget(self.comboBox_floodfill_color, 7, 3, 1, 1)
        self.label_resolution_out = QtWidgets.QLabel(self.groupBox_parameters)
        self.label_resolution_out.setObjectName("label_resolution_out")
        self.gridLayout_4.addWidget(self.label_resolution_out, 6, 1, 1, 1)
        self.label_dop_spacing = QtWidgets.QLabel(self.groupBox_parameters)
        self.label_dop_spacing.setObjectName("label_dop_spacing")
        self.gridLayout_4.addWidget(self.label_dop_spacing, 3, 1, 1, 1)
        self.label_sabre_angle_set = QtWidgets.QLabel(self.groupBox_parameters)
        self.label_sabre_angle_set.setObjectName("label_sabre_angle_set")
        self.gridLayout_4.addWidget(self.label_sabre_angle_set, 5, 3, 1, 1)
        self.label_resolution_set = QtWidgets.QLabel(self.groupBox_parameters)
        self.label_resolution_set.setObjectName("label_resolution_set")
        self.gridLayout_4.addWidget(self.label_resolution_set, 6, 3, 1, 1)
        self.checkBox_invert = QtWidgets.QCheckBox(self.groupBox_parameters)
        self.checkBox_invert.setObjectName("checkBox_invert")

        self.gridLayout_4.addWidget(self.checkBox_invert, 8, 1, 1, 1)
        
        self.label_floodfill_color = QtWidgets.QLabel(self.groupBox_parameters)
        self.label_floodfill_color.setObjectName("label_floodfill_color")
        self.gridLayout_4.addWidget(self.label_floodfill_color, 7, 1, 1, 1)
        self.spinBox_margin = QtWidgets.QSpinBox(self.groupBox_parameters)
        self.spinBox_margin.setMinimum(-100)
        self.spinBox_margin.setMaximum(100)
        self.spinBox_margin.setObjectName("spinBox_margin")
        self.gridLayout_4.addWidget(self.spinBox_margin, 2, 3, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.groupBox_parameters)
        self.pushButton.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_4.addWidget(self.pushButton, 7, 4, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_parameters, 1, 0, 1, 1)
        self.groupBox_path = QtWidgets.QGroupBox(self.groupBox_settings)
        self.groupBox_path.setObjectName("groupBox_path")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_path)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtWidgets.QLabel(self.groupBox_path)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 4, 0, 1, 1)
        self.label_dxf_path = QtWidgets.QLabel(self.groupBox_path)
        self.label_dxf_path.setObjectName("label_dxf_path")
        self.gridLayout_3.addWidget(self.label_dxf_path, 0, 0, 1, 1)
        self.toolButton_dxf_path = QtWidgets.QToolButton(self.groupBox_path)
        self.toolButton_dxf_path.setObjectName("toolButton_dxf_path")
        self.gridLayout_3.addWidget(self.toolButton_dxf_path, 0, 2, 1, 1)
        self.lineEdit_dxf_path = QtWidgets.QLineEdit(self.groupBox_path)
        self.lineEdit_dxf_path.setObjectName("lineEdit_dxf_path")
        self.gridLayout_3.addWidget(self.lineEdit_dxf_path, 0, 1, 1, 1)
        self.label_resolution_read = QtWidgets.QLabel(self.groupBox_path)
        self.label_resolution_read.setObjectName("label_resolution_read")
        self.gridLayout_3.addWidget(self.label_resolution_read, 1, 0, 1, 1)

        self.lineEdit_text_overlay = QtWidgets.QLineEdit(self.groupBox_textOverlay)
        self.lineEdit_text_overlay.setObjectName("lineEdit_text_overlay")
        self.lineEdit_text_overlay.setEnabled(False)
        self.gridLayout_7.addWidget(self.lineEdit_text_overlay, 1, 1, 1, 3)

        self.checkBox_text_overlay = QtWidgets.QCheckBox(self.groupBox_textOverlay)
        self.checkBox_text_overlay.setObjectName("checkBox_text_overlay")
        self.checkBox_text_overlay.setChecked(True)
        self.gridLayout_7.addWidget(self.checkBox_text_overlay, 0, 1, 1, 1)

        self.checkBox_text_overlay_custom = QtWidgets.QCheckBox(self.groupBox_textOverlay)
        self.checkBox_text_overlay_custom.setObjectName("checkBox_text_overlay_custom")
        self.checkBox_text_overlay_custom.setChecked(True)
        self.gridLayout_7.addWidget(self.checkBox_text_overlay_custom, 0, 2, 1, 2)

        self.label_text_size = QtWidgets.QLabel(self.groupBox_textOverlay)
        self.label_text_size.setObjectName("checkBox_text_overlay")
        self.gridLayout_7.addWidget(self.label_text_size, 2, 1, 1, 1)

        self.SpinBox_text_size = QtWidgets.QSpinBox(self.groupBox_textOverlay)
        self.SpinBox_text_size.setObjectName("SpinBox_text_size")
        self.SpinBox_text_size.setMinimum(0)
        self.SpinBox_text_size.setMaximum(100)
        self.SpinBox_text_size.setProperty("value", 5)
        self.gridLayout_7.addWidget(self.SpinBox_text_size, 2, 2, 1, 1)

        self.SpinBox_text_thickness = QtWidgets.QSpinBox(self.groupBox_textOverlay)
        self.SpinBox_text_thickness.setObjectName("SpinBox_text_thickness")
        self.SpinBox_text_thickness.setMinimum(1)
        self.SpinBox_text_thickness.setMaximum(100)
        self.SpinBox_text_thickness.setProperty("value", 1)
        self.gridLayout_7.addWidget(self.SpinBox_text_thickness, 2, 3, 1, 1)

        self.label_text_pos = QtWidgets.QLabel(self.groupBox_textOverlay)
        self.label_text_pos.setObjectName("label_text_pos")
        self.gridLayout_7.addWidget(self.label_text_pos, 3, 1, 1, 1)

        self.SpinBox_text_pos_x = QtWidgets.QSpinBox(self.groupBox_textOverlay)
        self.SpinBox_text_pos_x.setObjectName("SpinBox_text_pos_x")
        self.gridLayout_7.addWidget(self.SpinBox_text_pos_x, 3, 2, 1, 1)
        self.SpinBox_text_pos_x.setProperty("value", 50)

        self.SpinBox_text_pos_y = QtWidgets.QSpinBox(self.groupBox_textOverlay)
        self.SpinBox_text_pos_y.setObjectName("SpinBox_text_pos_y")
        self.gridLayout_7.addWidget(self.SpinBox_text_pos_y, 3, 3, 1, 1)
        self.SpinBox_text_pos_y.setProperty("value", 50)
        
        self.label_line_thickness = QtWidgets.QLabel(self.groupBox_path)
        self.label_line_thickness.setObjectName("label_line_thickness")
        self.gridLayout_3.addWidget(self.label_line_thickness, 2, 0, 1, 1)

        self.spinBox_dpi_read = QtWidgets.QSpinBox(self.groupBox_path)
        self.spinBox_dpi_read.setMinimum(1)
        self.spinBox_dpi_read.setMaximum(5080)
        self.spinBox_dpi_read.setProperty("value", 400)
        self.spinBox_dpi_read.setObjectName("spinBox_dpi_read")

        self.spinBox_line_thickness = QtWidgets.QSpinBox(self.groupBox_path)
        self.spinBox_line_thickness.setMinimum(1)
        self.spinBox_line_thickness.setMaximum(10)
        self.spinBox_line_thickness.setProperty("value", 2)
        self.spinBox_line_thickness.setObjectName("spinBox_line_thickness")

        self.gridLayout_3.addWidget(self.spinBox_dpi_read, 1, 1, 1, 1)
        self.gridLayout_3.addWidget(self.spinBox_line_thickness, 2, 1, 1, 1)

        self.pushButton_generate = QtWidgets.QPushButton(self.groupBox_path)
        self.pushButton_generate.setObjectName("pushButton_generate")
        self.gridLayout_3.addWidget(self.pushButton_generate, 3, 0, 1, 3)
        self.label_2 = QtWidgets.QLabel(self.groupBox_path)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 4, 1, 1, 2)
        self.gridLayout_2.addWidget(self.groupBox_path, 0, 0, 1, 1)

        self.label_license = QtWidgets.QLabel(self.groupBox_settings)
        self.label_license.setObjectName("label_license")
        self.gridLayout_2.addWidget(self.label_license, 5, 0, 1, 1)
        self.label_license.setEnabled(False)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 4, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_settings, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.graphicsView = QtWidgets.QGraphicsView(self.groupBox)
        self.graphicsView.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.mousePressEvent = self.mousePressEvent
        self.graphicsView.setBackgroundBrush(QtCore.Qt.gray)
        self.gridLayout_5.addWidget(self.graphicsView, 0, 0, 1, 1)

        self.gridLayout.addWidget(self.groupBox, 0, 1, 1, 1)
        dxf2bmp.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(dxf2bmp)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1073, 26))
        self.menubar.setObjectName("menubar")
        dxf2bmp.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(dxf2bmp)
        self.statusbar.setObjectName("statusbar")
        dxf2bmp.setStatusBar(self.statusbar)
        self.retranslateUi(dxf2bmp)
        QtCore.QMetaObject.connectSlotsByName(dxf2bmp)

        self.toolButton_dxf_path.clicked.connect(self.selectFile)
        self.pushButton_generate.clicked.connect(self.generateImage)
        self.spinBox_line_thickness.valueChanged.connect(self.generateImage)
        self.spinBox_margin.valueChanged.connect(self.generateImage)
        self.spinBox_dpi_read.valueChanged.connect(self.generateImage)
        self.pushButton.clicked.connect(self.Pick)
        self.pushButton_export.clicked.connect(self.export)
        self.toolButton_export_path.clicked.connect(self.SelectExportPath)
        self.checkBox_path.stateChanged.connect(self.dxf_path_check)
        self.SpinBox_text_pos_x.valueChanged.connect(self.generateImage)
        self.SpinBox_text_pos_y.valueChanged.connect(self.generateImage)
        self.SpinBox_text_size.valueChanged.connect(self.generateImage)
        self.lineEdit_text_overlay.textChanged.connect(self.generateImage)
        self.SpinBox_text_thickness.valueChanged.connect(self.generateImage)
        self.spinBox_drop_spacing.valueChanged.connect(self.generateImage)

        self.pushButton_generate.setEnabled(False)
        self.groupBox_parameters.setEnabled(False)
        self.groupBox_export.setEnabled(False)
        self.groupBox_textOverlay.setEnabled(False)
        self.comboBox_floodfill_color.setEnabled(False)
        
        self.pickFlag = False

        self.spinBox_drop_spacing.valueChanged.connect(self.DS_change)

        self.checkBox_invert.stateChanged.connect(self.invertImage)    
        self.checkBox_text_overlay.stateChanged.connect(self.toggle_text)
        self.checkBox_text_overlay_custom.stateChanged.connect(self.custom_text_overlay)

    def retranslateUi(self, dxf2bmp):
        _translate = QtCore.QCoreApplication.translate
        dxf2bmp.setWindowTitle(_translate("dxf2bmp", "dxf2bmp"))
        self.groupBox_settings.setTitle(_translate("dxf2bmp", "Settings"))
        self.groupBox_export.setTitle(_translate("dxf2bmp", "Export"))
        self.groupBox_textOverlay.setTitle(_translate("dxf2bmp", "Text overlay"))
        self.label_export_path.setText(_translate("dxf2bmp", "Export path"))
        self.toolButton_export_path.setText(_translate("dxf2bmp", "..."))
        self.pushButton_export.setText(_translate("dxf2bmp", "Export"))
        self.checkBox_path.setText(_translate("dxf2bmp", "Same as dxf path"))
        self.groupBox_parameters.setTitle(_translate("dxf2bmp", "Parameters"))
        self.label_sabre_angle.setText(_translate("dxf2bmp", "Sabre angle"+ "(" + u'\N{DEGREE SIGN}' + ")"))
        self.label_margin.setText(_translate("dxf2bmp", "Margin(Pixels)"))
        self.comboBox_floodfill_color.setItemText(0, _translate("dxf2bmp", "Black"))
        self.comboBox_floodfill_color.setItemText(1, _translate("dxf2bmp", "White"))
        self.label_resolution_out.setText(_translate("dxf2bmp", "Resolution(dpi)"))
        self.label_dop_spacing.setText(_translate("dxf2bmp", "Drop spacing(" +'\u03BC' + "m)"))
        self.label_sabre_angle_set.setText(_translate("dxf2bmp", "6.8"))
        self.label_resolution_set.setText(_translate("dxf2bmp", "847"))
        self.checkBox_invert.setText(_translate("dxf2bmp", "Invert"))
        self.checkBox_text_overlay.setText(_translate("dxf2bmp", "Show"))
        self.checkBox_text_overlay_custom.setText(_translate("dxf2bmp", "Default/Custom"))
        self.label_floodfill_color.setText(_translate("dxf2bmp", "Floodfill color"))
        self.pushButton.setText(_translate("dxf2bmp", "Pick"))
        self.groupBox_path.setTitle(_translate("dxf2bmp", "Read file"))
        self.label.setText(_translate("dxf2bmp", "Image size"))
        self.label_dxf_path.setText(_translate("dxf2bmp", "dxf path"))
        self.toolButton_dxf_path.setText(_translate("dxf2bmp", "..."))
        self.label_resolution_read.setText(_translate("dxf2bmp", "Resolution(dpi)"))
        self.label_line_thickness.setText(_translate("dxf2bmp", "Line Thickness"))
        self.pushButton_generate.setText(_translate("dxf2bmp", "Reset image"))
        self.label_2.setText(_translate("dxf2bmp", "0x0mm"))
        self.groupBox.setTitle(_translate("dxf2bmp", "Image view"))
        self.label_text_size.setText(_translate("dxf2bmp", "Text [size, thickness]"))
        self.label_text_pos.setText(_translate("dxf2bmp", "Text position[x,y]"))
        self.label_license.setText(_translate("dxf2bmp", "Copyright (c) 2023, Ahmed Albagdady"))

    def toggle_text(self):
        self.SpinBox_text_size.setEnabled(self.checkBox_text_overlay.checkState())
        self.SpinBox_text_pos_y.setEnabled(self.checkBox_text_overlay.checkState())
        self.SpinBox_text_pos_x.setEnabled(self.checkBox_text_overlay.checkState())
        self.SpinBox_text_thickness.setEnabled(self.checkBox_text_overlay.checkState())
        self.generateImage()

    def custom_text_overlay(self):
        self.lineEdit_text_overlay.setEnabled(not self.checkBox_text_overlay_custom.checkState())
        self.generateImage()

    def DS_change(self):
        alpha = np.arcsin(self.spinBox_drop_spacing.value()/254)
        self.label_sabre_angle_set.setText(str(np.round(np.degrees(alpha),1)))
        self.label_resolution_set.setText(str(int(25400/self.spinBox_drop_spacing.value())))

        if (self.spinBox_dpi_read.value() < int(self.label_resolution_set.text())):
            self.label_resolution_set.setStyleSheet("color: red;")

        elif (self.spinBox_dpi_read.value() >= int(self.label_resolution_set.text())):
            self.label_resolution_set.setStyleSheet("color: green;")
        else:
            self.label_resolution_set.setStyleSheet("color: black;")      

    def selectFile(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select dxf file", "", "Text files (*.dxf);;All files (*.*)")
        self.lineEdit_dxf_path.setText(file_path)
        self.generateImage()

    def dxf_path_check(self):
        self.lineEdit_export_path.setEnabled(not self.checkBox_path.isChecked())
        self.toolButton_export_path.setEnabled(not self.checkBox_path.isChecked())

    def SelectExportPath(self):
        file_path = QtWidgets.QFileDialog.getExistingDirectory(None, "Select export directory", "")    
        self.lineEdit_export_path.setText(file_path)

    def invertImage(self):
        self.Blank = 255-self.Blank
        #cv2.imshow("text",self.Blank)
        self.displayImage(self.Blank)        
        
    def generateImage(self):
        #The main function in this program, it reads the dxf file and redraw it on a blank white image.
        #Currelty only supports lines and arcs, therefore, polylines and cirlces must be exploded prior to loading

        try:
            # Try to read the dxf file from the path specified in lineEdit_dxf_path
            dxf = ezdxf.readfile(self.lineEdit_dxf_path.text())
            # Get the modelspace from the dxf file
            space = dxf.modelspace()


            # Enable all controls after reading the dxf file
            self.pushButton_generate.setEnabled(True)
            self.groupBox_parameters.setEnabled(True)
            self.groupBox_export.setEnabled(True)
            self.groupBox_textOverlay.setEnabled(True)
            self.checkBox_invert.setChecked(False)

            # Create empty arrays to store the attributes of lines and arcs
            Line = []
            Arc = []
            Xs = []
            Ys = []

            # Get the value of the spinBox_dpi_read control and convert it to dots per millimeter
            dpm = self.spinBox_dpi_read.value() / 25.4

            # Loop through the entities in the modelspace to store the attributes of lines and arcs
            for e in space:
                if e.dxftype() == "LINE":
                    # If the entity is a line, append its start and end points to the Line array
                    Line.append([[e.get_dxf_attrib('start'), e.get_dxf_attrib('end')]])
                    Lines = np.concatenate((Line), axis=0)
                if e.dxftype() == "ARC":
                    # If the entity is an arc, append its attributes to the Arc array
                    Arc_attr = ([[e.get_dxf_attrib('center'), e.get_dxf_attrib('radius'),
                                e.get_dxf_attrib('start_angle'), e.get_dxf_attrib('end_angle')]])
                    Arc.append([[Arc_attr[0][0][0], Arc_attr[0][0][1], Arc_attr[0][1], Arc_attr[0][2], Arc_attr[0][3]]])
                    Arcs = np.concatenate((Arc), axis=0)

            # Loop through the Lines array to get the minimum and maximum x and y values
            for L in Lines:
                Ys.append(L[0][1])
                Xs.append(L[0][0])
            Xmax = math.ceil(np.amax(Xs) * dpm)
            Xmin = math.floor(np.amin(Xs) * dpm)
            Ymax = math.ceil(np.amax(Ys) * dpm)
            Ymin = math.floor(np.amin(Ys) * dpm)

            # Create a blank image with the correct size
            self.Blank = np.ones(((Ymax - Ymin) + (2 * self.spinBox_margin.value()), (Xmax - Xmin) + (2 * self.spinBox_margin.value())), np.uint8) * 255
            # Create a mask with the same size as the blank image
            self.mask = np.zeros(((Ymax - Ymin) + (2 * self.spinBox_margin.value()) + 2, (Xmax - Xmin) + (2 * self.spinBox_margin.value()) + 2), np.uint8)

            # Set the text of label_2 to show the dimensions of the blank image
            self.label_2.setText(str(round(((Xmax - Xmin) + (2 * self.spinBox_margin.value())) / dpm)) + "x" + str(round(((Ymax - Ymin) + (2 * self.spinBox_margin.value())) / dpm)) + "mm")


            # Draw lines
            if Lines.size != 0:
                for L in Lines:
                    L[0][1] = round(L[0][1] * dpm - Ymin + self.spinBox_margin.value())
                    L[0][0] = round(L[0][0] * dpm - Xmin + self.spinBox_margin.value())
                    L[1][1] = round(L[1][1] * dpm - Ymin + self.spinBox_margin.value())
                    L[1][0] = round(L[1][0] * dpm - Xmin + self.spinBox_margin.value())

                    cv2.line(
                        self.Blank,
                        (int(L[0][0]), int(L[0][1])),
                        (int(L[1][0]), int(L[1][1])),
                        0,
                        thickness=self.spinBox_line_thickness.value()
                    ) 

            # Draw arcs
            if Arcs.size != 0:
                for A in Arcs:
                    A[0] = A[0] * dpm - Xmin + self.spinBox_margin.value() # Normalize CenterX
                    A[1] = A[1] * dpm - Ymin + self.spinBox_margin.value() # Normalize CenterY
                    A[2] = A[2] * dpm # Normalize Radius
                    startAng = A[3]
                    endAng = A[4]
                    A = A.astype(int)
                    self.Blank = self.DrawArc(self.Blank,(A[1], A[0]),A[2],startAng,endAng,0,100)

            # Set text position limits
            self.SpinBox_text_pos_x.setMinimum(0)
            self.SpinBox_text_pos_x.setMaximum(np.shape(self.Blank)[1])
            self.SpinBox_text_pos_y.setMinimum(0)
            self.SpinBox_text_pos_y.setMaximum(np.shape(self.Blank)[0])        

            # Extract filename from dxf path
            filename = self.lineEdit_dxf_path.text().split("/")

            # Draw text overlay if enabled
            if self.checkBox_text_overlay.isChecked():
                if self.checkBox_text_overlay_custom.isChecked():
                    text = filename[-1][:-4] + "_" + str(self.spinBox_dpi_read.value()) + "_" + str(self.spinBox_drop_spacing.value())  + "_" + self.label_2.text() + "_" + date.today().strftime("%d/%m/%Y")
                else:
                    text = self.lineEdit_text_overlay.text()

                cv2.putText(
                    self.Blank,
                    text,
                    (self.SpinBox_text_pos_x.value(), self.SpinBox_text_pos_y.value()),
                    cv2.FONT_HERSHEY_DUPLEX,self.SpinBox_text_size.value() / 10, (0, 0, 0), self.SpinBox_text_thickness.value(), cv2.LINE_AA)
        except:
            # If there was an error reading the file, print an error message and return
            print("File not loaded")
            return

        # Display image
        self.displayImage(self.Blank)

        # Set resolution label color
        if self.spinBox_dpi_read.value() < int(self.label_resolution_set.text()):
            self.label_resolution_set.setStyleSheet("color: red;")
        elif self.spinBox_dpi_read.value() >= int(self.label_resolution_set.text()):
            self.label_resolution_set.setStyleSheet("color: green;")
        else:
            self.label_resolution_set.setStyleSheet("color: black;")

    def displayImage(self,image):

        #This code segment creates an image viewer using the PyQt5 library. 
        #The image is first converted to a grayscale QImage object, and then to a QPixmap object. 
        #A QGraphicsPixmapItem is created and set with the QPixmap. 
        #A QGraphicsScene is created, and the QGraphicsPixmapItem is added to it. 
        #Finally, a QGraphicsView is created, and the QGraphicsScene is set to it. 
        #The result is an image viewer that displays the QPixmap object in the QGraphicsView. 
        #The last commented out line shows how to fit the view to the scene's rectangle while keeping the aspect ratio.

        #fix the size 

        qimage = QtGui.QImage(image, image.shape[1], image.shape[0], image.shape[1],QtGui.QImage.Format_Grayscale8)  
        # create a QPixmap from the QImage
        qpixmap = QtGui.QPixmap.fromImage(qimage)

        # create a QGraphicsPixmapItem and set its pixmap to the QPixmap
        pixmap_item = QtWidgets.QGraphicsPixmapItem(qpixmap)
        pixmap_item.setPos(-qpixmap.width(), -qpixmap.height())
    
        # create a QGraphicsScene and add the QGraphicsPixmapItem to it
        scene = QtWidgets.QGraphicsScene()
        scene.addItem(pixmap_item)

        # create a QGraphicsView and set its scene
        self.graphicsView.setScene(scene)
        #self.graphicsView.fitInView(scene.sceneRect(), QtCore.Qt.KeepAspectRatio) #aspect ratio
        self.graphicsView.show()

    def DrawArc(self,image, center, radius, startAng, endAng, color,resolution):
        '''
        The code takes in an image, center point, radius, start angle, end angle, color, and resolution as input. 
        It then calculates the angle between the start and end angles and adjusts the start and end angles to start at 90 degrees. 
        It generates an array of theta values and calculates the x and y values for each theta. Finally, it draws the arc using a series of lines and returns the modified image.

        Args:
        image      - The input image to draw the arc on
        center     - Arc's center
        radius     - Arc's radius
        startAng   - the starting angle of the arc
        engAng     - the ending angle of the arc
        color      - Arc's color on the input image
        resolution - Number of points for calculation

        output:
        image      - updated image with plotted arc'''


        # Calculate the angle between the start and end angles
        if startAng > endAng:
            fillAng = 360 - (startAng - endAng)
        else:
            fillAng = endAng - startAng
        
        # Adjust the start and end angles to start at 90 degrees
        endAng = startAng + fillAng
        startAng = 90 - startAng
        endAng = 90 - endAng 
        
        # Generate an array of theta values
        theta = np.linspace(startAng, endAng, resolution)

        # Calculate the x and y values for each theta
        x = np.round(radius * np.cos(np.deg2rad(theta)) + center[0])
        y = np.round(radius * np.sin(np.deg2rad(theta)) + center[1])
        x = x.astype(int)
        y = y.astype(int)

        # Draw the arc using a series of lines
        for k in range(np.size(theta) - 1):
            try:
                cv2.line(image, (y[k], x[k]), (y[k+1], x[k+1]), color, thickness=self.spinBox_line_thickness.value())
            except:
                pass
        
        # Calculate the x and y values for each theta again
        x = np.round(radius * np.cos(np.deg2rad(theta)) + center[0])
        y = np.round(radius * np.sin(np.deg2rad(theta)) + center[1])
        x = x.astype(int)
        y = y.astype(int)

        return image

    def mousePressEvent(self, event):
        # Check if left mouse button was clicked and pickFlag is set
        if (event.button() == QtCore.Qt.LeftButton) and (self.pickFlag):
            # Get the mouse position relative to the graphics view
            pos = self.graphicsView.mapToScene(event.pos())
            
            # Reset the cursor and apply flood fill to the Blank image
            self.graphicsView.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.Blank = self.floodFill(self.Blank,self.comboBox_floodfill_color.currentIndex(),pos.y(),pos.x())

            # Disable the pickFlag and update the image display
            self.pickFlag = False
            self.displayImage(self.Blank)

    def Pick(self): 
        if (self.pickFlag):
            self.pickFlag = False
            self.graphicsView.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        else:
            self.pickFlag = True
            self.graphicsView.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CrossCursor))

    def floodFill(self,image,newValue,mouseY,mouseX):
        # Get the dimensions of the input image
        shape = np.shape(image)

        # Make a copy of the input image
        input = image

        # Adjust the mouse coordinates to account for the image dimensions
        mouseY = shape[0] + mouseY
        mouseX = shape[1] + mouseX

        # Print the updated mouse coordinates and image dimensions
        print('x = %d, y = %d'%(mouseX, mouseY),np.shape(image))

        # Apply the flood fill algorithm to the input image using the updated mouse coordinates
        # The mask parameter specifies a binary mask used to restrict the filling area
        # The seedPoint parameter specifies the starting point for the fill operation
        # The newVal parameter specifies the color to be filled
        cv2.floodFill(image, mask=self.mask, seedPoint=(int(mouseX), int(mouseY)), newVal=(255*newValue))

        # Flip the image vertically
        image = np.flipud(image)
        
        return input
    
    def export(self):
        # Check if export path is not set but enabled
        if self.lineEdit_export_path.text() == "" and self.lineEdit_export_path.isEnabled():
            # Display warning message
            msg_box = QtWidgets.QMessageBox()
            msg_box.setWindowTitle('Warning')
            msg_box.setText('Set export path')
            msg_box.setIcon(QtWidgets.QMessageBox.Warning)
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg_box.exec()   
            # Return without exporting
            return

        # Convert the blank image to BMP format
        BMPout = Image.fromarray(self.Blank)

        # Calculate the resize factor based on the DPI read and resolution set
        Factor = self.spinBox_dpi_read.value()/int(self.label_resolution_set.text())

        # Calculate the new size based on the resize factor
        size = np.round(np.divide(np.shape(self.Blank),Factor))
        size = size.astype(int)

        # Resize and convert the image to binary format
        BMPout = BMPout.resize((size[1],size[0]))
        BMPout = BMPout.convert('1')

        # Extract the filename from the DXF path
        filename = self.lineEdit_dxf_path.text().split("/")

        # Generate the BMP path based on the filename and export settings
        if self.checkBox_path.isChecked():
            path = '/'.join(filename[:-1]) + "/" + filename[-1][:-4] + "_" + str(self.spinBox_dpi_read.value()) + "_" + str(self.spinBox_drop_spacing.value()) + "_" + str(self.spinBox_margin.value()) +".bmp"
        else:
            path = self.lineEdit_export_path.text() + "/" + filename[-1][:-4] + "_" + str(self.spinBox_dpi_read.value()) + "_" + str(self.spinBox_drop_spacing.value()) + "_" + str(self.spinBox_margin.value()) +".bmp"

        # Print the BMP export path for debugging purposes
        print(path)

        # Save the BMP file with the desired resolution
        BMPout.save(path ,dpi = (int(self.label_resolution_set.text()),int(self.label_resolution_set.text())))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dxf2bmp = QtWidgets.QMainWindow()
    ui = Ui_dxf2bmp()
    ui.setupUi(dxf2bmp)
    dxf2bmp.show()
    sys.exit(app.exec_())
