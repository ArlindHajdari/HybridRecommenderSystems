from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView, QMessageBox
import pandas as pd
from HRS import HybridRecommenderSystem
from Models.SessionUser import SessionUser


class Ui_MovieRecommenderMain(QtWidgets.QMainWindow, object):
    def __init__(self, parent=None):
        super(Ui_MovieRecommenderMain, self).__init__(parent)
        self.hrs = HybridRecommenderSystem()
        self.setupUi(self)
        self.parent = parent  # This is needed for the logout procedure (check: btnHome_Click)

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
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
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
        self.btnHome.clicked.connect(self.btnHome_Click)
        self.btnGenerate.clicked.connect(self.btnGenerate_Click)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icons/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnHome.setIcon(icon)
        self.btnHome.setIconSize(QtCore.QSize(20, 17))
        self.btnHome.setObjectName("btnHome")
        MovieRecommenderMain.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MovieRecommenderMain)
        self.statusbar.setObjectName("statusbar")
        MovieRecommenderMain.setStatusBar(self.statusbar)

        self.retranslateUi(MovieRecommenderMain)
        self.populateFriendList()
        QtCore.QMetaObject.connectSlotsByName(MovieRecommenderMain)

    def retranslateUi(self, MovieRecommenderMain):
        """ GUI text set for the elements """
        _translate = QtCore.QCoreApplication.translate
        MovieRecommenderMain.setWindowTitle(_translate("MovieRecommenderMain", "Movie Recommeder"))
        self.lblFriends.setText(_translate("MovieRecommenderMain", "Friends: "))
        self.btnGenerate.setText(_translate("MovieRecommenderMain", "Get recommendations"))
        self.lblRecommendedMovies.setText(_translate("MovieRecommenderMain", "Recommended movies"))

    def populateFriendList(self):
        """ Populate the ListWidget with users """

        # Suppose that 20 first rows are the friends of the logged in user
        friends = pd.read_csv("../data/users.csv", nrows=20)

        for index, row in friends.iterrows():
            if row[1] != SessionUser.username:  # Escape the logged in user (since he can not be friend with himself)
                item = QtWidgets.QListWidgetItem(row[1], self.friendsList)  # Set the display value of the ListWidget item
                item.setData(QtCore.Qt.UserRole, row[0])  # Set the value of the ListWidget item

    def btnHome_Click(self):
        """ Logout procedure """
        self.close()  # Close the current screen (Main)
        # Reset the textboxes
        self.parent.lbUsername.setText("")
        self.parent.lbPassword.setText("")

        # Show the login screen
        self.parent.show()

        # The logout procedure
        SessionUser.id = -1
        SessionUser.username = "none"

    def btnGenerate_Click(self):
        """ Generate the recommended movies from the selected users """

        # Get the selected users ids
        usersIds = [int(item.data(QtCore.Qt.UserRole)) for item in self.friendsList.selectedItems()]

        model = QtGui.QStandardItemModel()  # Initialize the model that is used by ListView

        if len(usersIds) > 0:  # Check if there are selected users
            # Add the current user to evaluate
            usersIds.insert(0, int(SessionUser.id))

            try:
                # The implementation of Hybrid recommender system
                recommended_movies = self.hrs.hybrid(usersIds)
                recommended_movies = recommended_movies['title'].values

                # Populate the model with the recommended movies titles
                for item in recommended_movies:
                    model.appendRow(QtGui.QStandardItem(item))
            except Exception as ex:
                QMessageBox.critical(self, 'Error', str(ex))
        else:
            QMessageBox.warning(self, 'Friends', "Please select your friends!", QMessageBox.Ok, QMessageBox.Ok)

        self.listView.setModel(model)  # ListView population
