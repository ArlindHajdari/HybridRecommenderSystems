from PyQt5 import QtWidgets
from LoginScreen import Ui_MovieRecommender_Window
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Ui_MovieRecommender_Window()
    MainWindow.show()
    sys.exit(app.exec_())