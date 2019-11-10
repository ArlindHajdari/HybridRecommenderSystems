# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoginScreen.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MovieRecommenderMain(QtWidgets.QMainWindow, object):
    def __init__(self, parent=None):
        super(Ui_MovieRecommenderMain, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, MovieRecommenderMain):
        MovieRecommenderMain.setObjectName("MovieRecommenderMain")
        MovieRecommenderMain.resize(590, 376)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MovieRecommenderMain.sizePolicy().hasHeightForWidth())
        MovieRecommenderMain.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MovieRecommenderMain)
        self.centralwidget.setObjectName("centralwidget")
        self.friendsList = QtWidgets.QListWidget(self.centralwidget)
        self.friendsList.setGeometry(QtCore.QRect(60, 30, 191, 281))
        self.friendsList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.friendsList.setMovement(QtWidgets.QListView.Static)
        self.friendsList.setWordWrap(True)
        self.friendsList.setObjectName("friendsList")
        self.lblFriends = QtWidgets.QLabel(self.centralwidget)
        self.lblFriends.setGeometry(QtCore.QRect(10, 30, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lblFriends.setFont(font)
        self.lblFriends.setObjectName("lblFriends")
        self.btnGenerate = QtWidgets.QPushButton(self.centralwidget)
        self.btnGenerate.setGeometry(QtCore.QRect(60, 320, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnGenerate.setFont(font)
        self.btnGenerate.setObjectName("btnGenerate")
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(260, 60, 321, 251))
        self.listView.setObjectName("listView")
        self.lblRecommendedMovies = QtWidgets.QLabel(self.centralwidget)
        self.lblRecommendedMovies.setGeometry(QtCore.QRect(260, 30, 321, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lblRecommendedMovies.setFont(font)
        self.lblRecommendedMovies.setAlignment(QtCore.Qt.AlignCenter)
        self.lblRecommendedMovies.setObjectName("lblRecommendedMovies")
        self.btnHome = QtWidgets.QPushButton(self.centralwidget)
        self.btnHome.setGeometry(QtCore.QRect(10, 0, 31, 23))
        self.btnHome.setText("")
        self.btnHome.clicked.connect(self.btnHome_onClick)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnHome.setIcon(icon)
        self.btnHome.setIconSize(QtCore.QSize(20, 17))
        self.btnHome.setObjectName("btnHome")
        MovieRecommenderMain.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MovieRecommenderMain)
        self.statusbar.setObjectName("statusbar")
        MovieRecommenderMain.setStatusBar(self.statusbar)

        self.retranslateUi(MovieRecommenderMain)
        QtCore.QMetaObject.connectSlotsByName(MovieRecommenderMain)

    def retranslateUi(self, MovieRecommenderMain):
        _translate = QtCore.QCoreApplication.translate
        MovieRecommenderMain.setWindowTitle(_translate("MovieRecommenderMain", "Movie Recommeder"))
        self.lblFriends.setText(_translate("MovieRecommenderMain", "Friends: "))
        self.btnGenerate.setText(_translate("MovieRecommenderMain", "Generate"))
        self.lblRecommendedMovies.setText(_translate("MovieRecommenderMain", "Recommended movies"))

    def btnHome_onClick(self):
        print("Home button clicked!")