import os
import sys
import savefile
import datasheets
from win32gui import GetWindowText, GetForegroundWindow
from mainWindow import Ui_MainWindow
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pathlib import Path


def calculated_save_file_path() -> str:
    r"""
    Tries to find a save-file location and returns a path to it.
    Standard save file location:
    C:\Users(username)\AppData\Roaming\EldenRing\(SteamID)\ER0000.sl2
    :return: blank string if file wasn't found
    """

    elden_ring_path = str(Path.home()) + '\\AppData\\Roaming\\EldenRing'

    if not os.path.exists(elden_ring_path):
        return ''

    # Looking for a folder with a name like "7xxxxxxxxxxxxxxxx"
    steam_id_folder = ''
    file_names = os.listdir(elden_ring_path)
    for file_name in file_names:
        if len(file_name) == 17 and file_name.startswith('7'):
            steam_id_folder = file_name
            break

    if not steam_id_folder:
        return ''

    save_file_path = f'{elden_ring_path}\\{steam_id_folder}\\ER0000.sl2'

    if not os.path.exists(save_file_path):
        return ''

    return save_file_path


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.save_file_location = ''

        self.init_ui()

        # Here must be an attempt to get things from outer file.
        # self.read_settings()

        if not self.save_file_location:
            self.save_file_location = calculated_save_file_path()

        self.after_save_file_location_changing()

        self.show()

    def init_ui(self):
        """

        """
        self.setupUi(self)

        self.center_window()
        self.button_OpenSaveFile.clicked.connect(self.open_save_file)

    def after_save_file_location_changing(self):
        """

        """

        # Init save-slots.
        self.comboBox_SaveSlots.clear()
        if self.save_file_location:
            names = savefile.get_slot_names(self.save_file_location)
            for i, name in enumerate(names, 1):
                if name:
                    self.comboBox_SaveSlots.addItem(f'{i}. {name}')
        else:
            self.comboBox_SaveSlots.addItem('< Choose save file! >')

    def open_save_file(self):
        """

        :return:
        """

        start_folder = str(Path.home())

        if self.save_file_location:
            start_folder = '\\'.join(self.save_file_location.split('\\')[:-1])
        elif os.path.exists(
                str(Path.home()) + '\\AppData\\Roaming\\EldenRing'):
            start_folder = str(Path.home()) + '\\AppData\\Roaming\\EldenRing'

        options = QFileDialog.Options()
        location, _ = QFileDialog.getOpenFileName(self,
                                                  "Choose your Elden Ring Save File",
                                                  start_folder,
                                                  "Elden Ring Save File (*.sl2)",
                                                  options=options)

        if location:
            self.save_file_location = location
            self.after_save_file_location_changing()

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def start_application():
    """

    """

    app = QApplication(sys.argv)

    window = MainWindow()
    window.setWindowTitle('How would I call it?')
    # window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_application()

    # keyboard.add_hotkey('ctrl+p', lambda: print('You pressed p'))
    # keyboard.add_hotkey('o', lambda _: sort_all_lists())
    # # For catching keyboard presses.
    # with Listener(on_press=on_press) as listener:
    #     listener.join()
