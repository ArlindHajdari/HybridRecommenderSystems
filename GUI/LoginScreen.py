import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from MainScreen import Ui_MovieRecommenderMain
import pandas as pd
from Models.SessionUser import SessionUser

chunksize = 10 ** 6


# region [Old exception behaviour (PyQt4.0)]
# The PyQt5.0 exceptions, terminate the GUI application
# In order to stop that we handle it with the following code:
def my_excepthook(type, value, tback):
    # log the exception here

    # then call the default handler
    sys.__excepthook__(type, value, tback)


sys.excepthook = my_excepthook
# endregion

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
        """ GUI text set for the elements """
        _translate = QtCore.QCoreApplication.translate
        MovieRecommender_Window.setWindowTitle(_translate("MovieRecommender_Window", "Movie Recommeder"))
        self.lbUsername.setPlaceholderText(_translate("MovieRecommender_Window", "Username"))
        self.lbPassword.setPlaceholderText(_translate("MovieRecommender_Window", "Password"))
        self.btnSubmit.setText(_translate("MovieRecommender_Window", "Submit"))
        self.lbLogin.setText(_translate("MovieRecommender_Window", "Login"))

    def userExists(self):
        """ User check in the dataset
            returns empty dataframe on error, the matched row if credentials match"""
        if self.lbUsername.text() is "" or self.lbPassword.text() is "":
            return pd.DataFrame()

        # Check for the typed credentials on a chunk separated dataset (chunksize = 1.000.000 bytes)
        # For a better performance if the user exists at the beginning, the same if exists at the end of the dataset
        for chunk in pd.read_csv("../data/users.csv", dtype=str, chunksize=chunksize):
            row_found = chunk.loc[(chunk.userNames == self.lbUsername.text()) & (chunk.password == self.lbPassword.text())]
            if not row_found.empty:
                return row_found

        return pd.DataFrame()

    def onSubmit(self):
        """ Login procedure """

        userBeing = self.userExists()
        if userBeing.empty:
            QMessageBox.warning(self, 'LOGIN', "Please type the right information!", QMessageBox.Ok, QMessageBox.Ok)
            return

        # Set the session static class with the logged in user details
        SessionUser.id = userBeing.id.values[0]
        SessionUser.username = userBeing.userNames[0]

        main = Ui_MovieRecommenderMain(self)  # Initialize the new screen
        self.close()  # Close the current screen(Login screen)
        main.show()  # Show the Main screen
