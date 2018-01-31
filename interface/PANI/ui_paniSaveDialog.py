# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'paniSaveDialog.ui'
#
# Created: Fri Jun 22 15:34:48 2012
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_NanotubeSaveDialog(object):
    def setupUi(self, NanotubeSaveDialog):
        NanotubeSaveDialog.setObjectName(_fromUtf8("NanotubeSaveDialog"))
        NanotubeSaveDialog.resize(400, 403)
        self.verticalLayoutWidget = QtGui.QWidget(NanotubeSaveDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 401, 401))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Nimbus Roman No9 L"))
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.frame = QtGui.QFrame(self.verticalLayoutWidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.browsePDBButton = QtGui.QPushButton(self.frame)
        self.browsePDBButton.setGeometry(QtCore.QRect(280, 30, 97, 27))
        self.browsePDBButton.setObjectName(_fromUtf8("browsePDBButton"))
        self.pdbFilename = QtGui.QLineEdit(self.frame)
        self.pdbFilename.setGeometry(QtCore.QRect(30, 30, 211, 27))
        self.pdbFilename.setObjectName(_fromUtf8("pdbFilename"))
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(160, 10, 67, 17))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Nimbus Roman No9 L"))
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.frame)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.frame_2 = QtGui.QFrame(self.verticalLayoutWidget)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.label_3 = QtGui.QLabel(self.frame_2)
        self.label_3.setGeometry(QtCore.QRect(160, 10, 67, 17))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Nimbus Roman No9 L"))
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.browsePSFButton = QtGui.QPushButton(self.frame_2)
        self.browsePSFButton.setGeometry(QtCore.QRect(280, 30, 97, 27))
        self.browsePSFButton.setObjectName(_fromUtf8("browsePSFButton"))
        self.psfFilename = QtGui.QLineEdit(self.frame_2)
        self.psfFilename.setGeometry(QtCore.QRect(30, 30, 211, 27))
        self.psfFilename.setObjectName(_fromUtf8("psfFilename"))
        self.label_4 = QtGui.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(20, 70, 371, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Nimbus Roman No9 L"))
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_3.addWidget(self.frame_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancelButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.okButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout.addWidget(self.okButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(NanotubeSaveDialog)
        QtCore.QMetaObject.connectSlotsByName(NanotubeSaveDialog)

    def retranslateUi(self, NanotubeSaveDialog):
        NanotubeSaveDialog.setWindowTitle(QtGui.QApplication.translate("NanotubeSaveDialog", "Save coordinates", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NanotubeSaveDialog", "Save coordinates and topology", None, QtGui.QApplication.UnicodeUTF8))
        self.browsePDBButton.setText(QtGui.QApplication.translate("NanotubeSaveDialog", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NanotubeSaveDialog", "PDF file", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("NanotubeSaveDialog", "PSF file", None, QtGui.QApplication.UnicodeUTF8))
        self.browsePSFButton.setText(QtGui.QApplication.translate("NanotubeSaveDialog", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("NanotubeSaveDialog", "(leaving this field empty inhibiths psf file generation)", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("NanotubeSaveDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("NanotubeSaveDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))

