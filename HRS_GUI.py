from LoginScreen import Ui_MovieRecommender_Window
from PyQt5 import QtWidgets

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Ui_MovieRecommender_Window()
    MainWindow.show()
    sys.exit(app.exec_())