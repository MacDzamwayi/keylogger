from PyQt6 import QtWidgets, QtCore, QtGui
import sys
import warnings
from Storage.database import pull_json, push_json, delete_json
from Ui_design import Ui_MainWindow, InputDialog


class Logic(QtWidgets.QMainWindow):
    def __init__(self, storage):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.dialog = InputDialog()
        self.storage = storage
        self.ui.setupUi(self)
        self.ui.createButton.clicked.connect(lambda _, name=None: self.handle_create(name))
        self.ui.onOffButtonD2.clicked.connect(self.toggle_recording)
        self.ui.bake_button.clicked.connect(self.handle_bake)
        self.ui.button_show.clicked.connect(self.toggle_displaying)
        self.ui.saveButton.clicked.connect(self.handle_save)
        self.ui.activateButton.clicked.connect(self.activate)
        self.ui.deleteButton.clicked.connect(self.handle_delete)
        self.button_group = QtWidgets.QButtonGroup(self)
        self.button_group.setExclusive(True)  # only one can stay checked
        self.button_group.buttonClicked.connect(self.set_current_button)
        self.load_buttons()

    def handle_create(self, name):
        if name is None:
            self.value = self.dialog.get_value()
        else:
            self.value = name

        if self.value is None or self.value.replace(' ', '') == '':
            return

        new_btn = QtWidgets.QPushButton(self.value, parent=self.ui.verticalLayoutWidget)
        new_btn.setCheckable(True)
        new_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid white;
                background: gray;
                color: black;
            }
            QPushButton:checked {
                background: white;
                border: 1px solid black;
            }
        """)

        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(12)
        font.setBold(False)
        font.setKerning(True)
        new_btn.setFont(font)

        # Add to layout
        self.ui.verticalLayout.insertWidget(0, new_btn)

        # Add to button group (so exclusivity is handled automatically)
        self.button_group.addButton(new_btn)

        # Save to JSON if this is a new creation
        if name is None:
            self.storage.update({
                self.value: [
                    self.ui.entryC2.text(),
                    self.ui.labelB2.text(),
                    self.ui.labelA2.text()
                ]
            })
        new_btn.clicked.connect(lambda _, b=new_btn: self.set_current_button(b))
        print('create')

    def toggle_recording(self):
        # Get reference to the last button you interacted with
        if not hasattr(self, "current_button"):
            if self.ui.onOffButtonD2.text().lower() == "off":
                self.ui.onOffButtonD2.setText("ON")
            else:
                self.ui.onOffButtonD2.setText("OFF")
            return  # no button selected yet

        if self.ui.onOffButtonD2.text().lower() == "off":
            self.ui.onOffButtonD2.setText("ON")
            print('on')
        else:
            self.ui.onOffButtonD2.setText("OFF")


    def handle_bake(self):
        # Get reference to the last button you interacted with
        if not hasattr(self, "current_button"):
            return  # no button selected yet
        print('Trojan Created')

    def toggle_displaying(self):
        # Get reference to the last button you interacted with
        if not hasattr(self, "current_button"):
            if self.ui.button_show.isChecked():
                self.ui.button_show.setText('ON')

            else:
                self.ui.button_show.setText('OFF')
            return  # no button selected yet
        if self.ui.button_show.isChecked():
            self.ui.button_show.setText('ON')
            self.display()

        else:
            self.ui.button_show.setText('OFF')

    def handle_save(self):
        # Get reference to the last button you interacted with
        if not hasattr(self, "current_button"):
            return  # no button selected yet
        port = int(self.ui.entryC2.text()) if self.ui.entryC2.text() else None
        if port is None:
            self.ui.statusbar.showMessage("ALERT: Please enter Port Number", 5000)
            return 0
        updated_list = self.storage.get(self.current_button.text())
        updated_list[0] = port
        self.storage[self.current_button.text()] = updated_list
        push_json(self.storage)
        print('save')

    def activate(self):
        # Get reference to the last button you interacted with
        if not hasattr(self, "current_button"):
            if self.ui.activateButton.isChecked():
                self.ui.activateButton.setText('ACTIVATED')

            else:
                self.ui.activateButton.setText('DEACTIVATED')
            return  # no button selected yet
        if self.ui.activateButton.isChecked():
            self.ui.activateButton.setText('ACTIVATED')

        else:
            self.ui.activateButton.setText('DEACTIVATED')
        print('activate')

    def handle_delete(self):
        """Delete the currently selected/active button and update JSON."""

        # Get reference to the last button you interacted with
        if not hasattr(self, "current_button"):
            return  # no button selected yet

        button = self.current_button
        label = button.text()

        # Remove from layout/UI
        self.ui.verticalLayout.removeWidget(button)
        button.deleteLater()

        # Remove from JSON

        if label in self.storage:
            del self.storage[label]
            delete_json(label)

        # Reset current button
        self.current_button = None
        print('delete')

    def handle_newButton(self):
        _translate = QtCore.QCoreApplication.translate
        if self.current_button.isChecked():
            self.ui.entryC2.setText(_translate("MainWindow", f"{self.storage.get(self.current_button.text())[0]}"))
            self.ui.labelB2.setText(_translate("MainWindow", f"{self.storage.get(self.current_button.text())[1]}"))
            self.ui.labelA2.setText(_translate("MainWindow", f"{self.storage.get(self.current_button.text())[2]}"))

    def load_buttons(self):
        """Load buttons from JSON"""
        if self.storage.keys() is None:
            return
        for label in self.storage.keys():
            self.handle_create(label)

    def display(self):
        self.max_lines = 15  # keep only last 50 messages
        self.lines = []

        self.counter = 0
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_label)
        self.timer.start(500)

    def update_label(self):
        self.counter += 1
        self.lines.append(
            f'Hello nigga vbvoewof weiweivwve wivw vief oqe qoeivbiqev qeqiebr uqererg ejrgergq '
            f'iergire riqbeiur'
            f'pgirgwrh wjruf equgvy erifgejh uguerg wiiurbghh rgubrh rgwiurg wruru\n {self.counter}')
        if len(self.lines) > self.max_lines:
            self.lines.pop(0)

        # Save scrollbar state *before* updating
        scrollbar = self.ui.Viewlabel.verticalScrollBar()
        at_bottom = scrollbar.value() == scrollbar.maximum()

        # Update text
        self.ui.Viewlabel.setPlainText("\n".join(self.lines))

        # Restore scroll only if user was at bottom
        if at_bottom:
            scrollbar.setValue(scrollbar.maximum())

    def set_current_button(self, button):
        """Mark the button as the currently active one for delete operations."""
        self.current_button = button
        self.handle_newButton()  # still call your existing function


if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    app = QtWidgets.QApplication(sys.argv)
    storage = pull_json()
    MainWindow = Logic(storage)
    MainWindow.show()
    sys.exit(app.exec())
