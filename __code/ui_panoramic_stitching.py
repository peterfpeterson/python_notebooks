# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/j35/git/python_notebooks/ui/ui_panoramic_stitching.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1013, 819)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.widget = QtWidgets.QWidget(self.splitter_2)
        self.widget.setObjectName("widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.splitter = QtWidgets.QSplitter(self.widget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.splitter_3 = QtWidgets.QSplitter(self.splitter)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.groupBox_2 = QtWidgets.QGroupBox(self.splitter_3)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.reference_widget = QtWidgets.QWidget(self.groupBox_2)
        self.reference_widget.setObjectName("reference_widget")
        self.horizontalLayout_3.addWidget(self.reference_widget)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.groupBox = QtWidgets.QGroupBox(self.splitter_3)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.target_widget = QtWidgets.QWidget(self.groupBox)
        self.target_widget.setObjectName("target_widget")
        self.horizontalLayout_2.addWidget(self.target_widget)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tableWidget = QtWidgets.QTableWidget(self.splitter)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.verticalLayout_4.addWidget(self.splitter)
        self.run_stitching_button = QtWidgets.QPushButton(self.widget)
        self.run_stitching_button.setObjectName("run_stitching_button")
        self.verticalLayout_4.addWidget(self.run_stitching_button)
        self.groupBox_3 = QtWidgets.QGroupBox(self.splitter_2)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.stitched_widget = QtWidgets.QWidget(self.groupBox_3)
        self.stitched_widget.setObjectName("stitched_widget")
        self.verticalLayout_3.addWidget(self.stitched_widget)
        self.stitched_table = QtWidgets.QTableWidget(self.groupBox_3)
        self.stitched_table.setObjectName("stitched_table")
        self.stitched_table.setColumnCount(0)
        self.stitched_table.setRowCount(0)
        self.verticalLayout_3.addWidget(self.stitched_table)
        self.verticalLayout_5.addWidget(self.splitter_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cancel_button = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.export_button = QtWidgets.QPushButton(self.centralwidget)
        self.export_button.setObjectName("export_button")
        self.horizontalLayout.addWidget(self.export_button)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1013, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.cancel_button.clicked.connect(MainWindow.cancel_clicked)
        self.export_button.clicked.connect(MainWindow.apply_clicked)
        self.tableWidget.itemSelectionChanged.connect(MainWindow.table_widget_selection_changed)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Reference Image"))
        self.groupBox.setTitle(_translate("MainWindow", "Target Image"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Reference Images"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Target Images"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Status"))
        self.run_stitching_button.setText(_translate("MainWindow", "Run Stitching "))
        self.groupBox_3.setTitle(_translate("MainWindow", "Stiched Image"))
        self.cancel_button.setText(_translate("MainWindow", "Close"))
        self.export_button.setText(_translate("MainWindow", "Export ..."))

