# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/j35/git/IPTS/python_notebooks/ui/ui_addie.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1352, 807)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.h1_table = QtWidgets.QTableWidget(self.frame)
        self.h1_table.setMinimumSize(QtCore.QSize(0, 20))
        self.h1_table.setMaximumSize(QtCore.QSize(16777215, 20))
        self.h1_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.h1_table.setAutoScroll(True)
        self.h1_table.setObjectName("h1_table")
        self.h1_table.setColumnCount(0)
        self.h1_table.setRowCount(0)
        self.verticalLayout.addWidget(self.h1_table)
        self.h2_table = QtWidgets.QTableWidget(self.frame)
        self.h2_table.setMinimumSize(QtCore.QSize(0, 20))
        self.h2_table.setMaximumSize(QtCore.QSize(16777215, 20))
        self.h2_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.h2_table.setObjectName("h2_table")
        self.h2_table.setColumnCount(5)
        self.h2_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.h2_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.h2_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.h2_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.h2_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.h2_table.setHorizontalHeaderItem(4, item)
        self.verticalLayout.addWidget(self.h2_table)
        self.h3_table = QtWidgets.QTableWidget(self.frame)
        self.h3_table.setBaseSize(QtCore.QSize(0, 0))
        self.h3_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.h3_table.setAlternatingRowColors(True)
        self.h3_table.setObjectName("h3_table")
        self.h3_table.setColumnCount(8)
        self.h3_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.h3_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.h3_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.h3_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.h3_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.h3_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.h3_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.h3_table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.h3_table.setHorizontalHeaderItem(7, item)
        self.verticalLayout.addWidget(self.h3_table)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout.addWidget(self.frame)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setMinimumSize(QtCore.QSize(250, 0))
        self.treeWidget.setMaximumSize(QtCore.QSize(250, 16777215))
        self.treeWidget.setObjectName("treeWidget")
        self.verticalLayout_2.addWidget(self.treeWidget)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1352, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.h3_table.customContextMenuRequested['QPoint'].connect(MainWindow.h3_table_right_click)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.h2_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Runs"))
        item = self.h2_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Background"))
        item = self.h2_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Packing Fraction"))
        item = self.h2_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Geometry"))
        item = self.h3_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Runs"))
        item = self.h3_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Background Runs"))
        item = self.h3_table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Shape"))
        item = self.h3_table.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Radius"))
        item = self.h3_table.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Height"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "Columns Visibility"))

