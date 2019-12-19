# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoginScreen.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from MainScreen import Ui_MovieRecommenderMain
import pandas as pd
from Models.SessionUser import SessionUser

class Ui_MovieRecommender_Window(QtWidgets.QMainWindow, object):
    def __init__(self, parent=None):
        super(Ui_MovieRecommender_Window, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, MovieRecommender_Window):
        MovieRecommender_Window.setObjectName("MovieRecommender_Window")
        MovieRecommender_Window.resize(527, 433)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MovieRecommender_Window.sizePolicy().hasHeightForWidth())
        MovieRecommender_Window.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MovieRecommender_Window)
        self.centralwidget.setObjectName("centralwidget")
        self.lbUsername = QtWidgets.QLineEdit(self.centralwidget)
        self.lbUsername.setGeometry(QtCore.QRect(180, 160, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lbUsername.setFont(font)
        self.lbUsername.setObjectName("lbUsername")
        self.lbPassword = QtWidgets.QLineEdit(self.centralwidget)
        self.lbPassword.setGeometry(QtCore.QRect(180, 220, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lbPassword.setFont(font)
        self.lbPassword.setInputMethodHints(QtCore.Qt.ImhSensitiveData)
        self.lbPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lbPassword.setObjectName("lbPassword")
        self.btnSubmit = QtWidgets.QPushButton(self.centralwidget)
        self.btnSubmit.setGeometry(QtCore.QRect(180, 290, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.btnSubmit.clicked.connect(self.onSubmit)
        self.btnSubmit.setFont(font)
        self.btnSubmit.setObjectName("btnSubmit")
        self.lbPassword.returnPressed.connect(self.btnSubmit.click)
        self.lbUsername.returnPressed.connect(self.btnSubmit.click)
        self.lbLogin = QtWidgets.QLabel(self.centralwidget)
        self.lbLogin.setGeometry(QtCore.QRect(180, 70, 181, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(False)
        font.setWeight(50)
        self.lbLogin.setFont(font)
        self.lbLogin.setTextFormat(QtCore.Qt.RichText)
        self.lbLogin.setAlignment(QtCore.Qt.AlignCenter)
        self.lbLogin.setObjectName("lbLogin")
        MovieRecommender_Window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MovieRecommender_Window)
        self.statusbar.setObjectName("statusbar")
        MovieRecommender_Window.setStatusBar(self.statusbar)

        self.retranslateUi(MovieRecommender_Window)
        QtCore.QMetaObject.connectSlotsByName(MovieRecommender_Window)

    def retranslateUi(self, MovieRecommender_Window):
        _translate = QtCore.QCoreApplication.translate
        MovieRecommender_Window.setWindowTitle(_translate("MovieRecommender_Window", "Movie Recommeder"))
        self.lbUsername.setPlaceholderText(_translate("MovieRecommender_Window", "Username"))
        self.lbPassword.setPlaceholderText(_translate("MovieRecommender_Window", "Password"))
        self.btnSubmit.setText(_translate("MovieRecommender_Window", "Submit"))
        self.lbLogin.setText(_translate("MovieRecommender_Window", "Login"))

    def userExists(self):
        """ User check in the dataset """
        if self.lbUsername.text() is "" or self.lbPassword.text() is "":
            return pd.DataFrame()

        usersDF = pd.read_csv("../data/users.csv", dtype=str)
        SessionUser.users_dataset = usersDF
        return usersDF.loc[(usersDF.userNames == self.lbUsername.text()) & (usersDF.password == self.lbPassword.text())]

    def onSubmit(self):
        userBeing = self.userExists()
        if userBeing.empty:
            QMessageBox.warning(self, 'LOGIN', "Please type the right information!", QMessageBox.Ok, QMessageBox.Ok)
            return

        SessionUser.id = userBeing.id.values[0]
        SessionUser.username = userBeing.userNames[0]
        
        main = Ui_MovieRecommenderMain(self)
        self.close()
        main.show()