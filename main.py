import warnings
import sys
from PyQt6 import QtWidgets
from Storage.database import pull_json
from User_interface.Ui_logic import Logic


def main():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    app = QtWidgets.QApplication(sys.argv)
    storage = pull_json()
    MainWindow = Logic(storage)
    MainWindow.show()
    sys.exit(app.exec())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
