# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ImportMolecules.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ImportMolecules(object):
    def setupUi(self, ImportMolecules):
        ImportMolecules.setObjectName("ImportMolecules")
        ImportMolecules.resize(331, 135)
        self.layoutWidget = QtWidgets.QWidget(ImportMolecules)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 312, 119))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pdbRButton = QtWidgets.QRadioButton(self.layoutWidget)
        self.pdbRButton.setChecked(True)
        self.pdbRButton.setObjectName("pdbRButton")
        self.horizontalLayout.addWidget(self.pdbRButton)
        self.sdfRButton = QtWidgets.QRadioButton(self.layoutWidget)
        self.sdfRButton.setObjectName("sdfRButton")
        self.horizontalLayout.addWidget(self.sdfRButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.IDlineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.IDlineEdit.setObjectName("IDlineEdit")
        self.horizontalLayout_3.addWidget(self.IDlineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(78, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.ok = QtWidgets.QPushButton(self.layoutWidget)
        self.ok.setObjectName("ok")
        self.horizontalLayout_4.addWidget(self.ok)
        self.cancel = QtWidgets.QPushButton(self.layoutWidget)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout_4.addWidget(self.cancel)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(ImportMolecules)
        QtCore.QMetaObject.connectSlotsByName(ImportMolecules)

    def retranslateUi(self, ImportMolecules):
        _translate = QtCore.QCoreApplication.translate
        ImportMolecules.setWindowTitle(_translate("ImportMolecules", "Import molecules"))
        self.label.setText(_translate("ImportMolecules", "Import molecules from:"))
        self.pdbRButton.setText(_translate("ImportMolecules", "Protein Data Bank"))
        self.sdfRButton.setText(_translate("ImportMolecules", "NCI-CADD Group"))
        self.label_2.setText(_translate("ImportMolecules", "File ID:"))
        self.ok.setText(_translate("ImportMolecules", "Ok"))
        self.cancel.setText(_translate("ImportMolecules", "Cancel"))

