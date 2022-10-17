import os
import sys
import savefile
from win32gui import GetWindowText, GetForegroundWindow
from mainWindow import Ui_MainWindow
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pathlib import Path


def available_hotkey_buttons() -> tuple:
    """
    List of keyboard buttons that can be used for hotkey assign.
    [0] - for user.
    [1] - for inner use.
    """

    return (
        ("F1", "F1"),
        ("F2", "F2"),
        ("F3", "F3"),
        ("F4", "F4"),
        ("F5", "F5"),
        ("F6", "F6"),
        ("F7", "F7"),
        ("F8", "F8"),
        ("F9", "F9"),
        ("F10", "F10"),
        ("F11", "F11"),
        ("F12", "F12"),
        ("0", "0"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("Num0", "Num0"),
        ("Num1", "Num1"),
        ("Num2", "Num2"),
        ("Num3", "Num3"),
        ("Num4", "Num4"),
        ("Num5", "Num5"),
        ("Num6", "Num6"),
        ("Num7", "Num7"),
        ("Num8", "Num8"),
        ("Num9", "Num9"),
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("E", "E"),
        ("F", "F"),
        ("G", "G"),
        ("H", "H"),
        ("I", "I"),
        ("J", "J"),
        ("K", "K"),
        ("L", "L"),
        ("M", "M"),
        ("N", "N"),
        ("O", "O"),
        ("P", "P"),
        ("Q", "Q"),
        ("R", "R"),
        ("S", "S"),
        ("T", "T"),
        ("U", "U"),
        ("V", "V"),
        ("W", "W"),
        ("X", "X"),
        ("Y", "Y"),
        ("Z", "Z"),
        ("Tab", "Tab"),
        ("Shift (left)", "Shift (left)"),
        ("Shift (right)", "Shift (right)"),
        ("Control (left)", "Control (left)"),
        ("Control (right)", "Control (right)"),
        ("Space", "Space"),
        ("Backspace", "Backspace"),
        ("Enter (main)", "Enter (main)"),
        ("Enter (numpad)", "Enter (numpad)"),
        ("Alt (left)", "Alt (left)"),
        ("Home", "Home"),
        ("PageUp", "PageUp"),
        ("End", "End"),
        ("PageDown", "PageDown"),
        ("Insert", "Insert"),
        ("Delete", "Delete")
    )



class SaveSlot:
    """

    """
    def __init__(self):

        self.id = ''
        self.name = ''
        self.weapon_list = []
        self.armor_head_list = []
        self.armor_torso_list = []
        self.armor_hands_list = []
        self.armor_legs_list = []
        self.talisman_list = []
        self.spell_list = []
        self.item_list = []


class Macro:
    """

    """

    def __init__(self):

        self.id = ''
        self.name = ''
        self.type = ''
        self.hotkey = ''
        self.hotkey_ctrl = False
        self.hotkey_shift = False
        self.hotkey_alt = False


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.save_file_location = ''
        self.save_slots = []
        self.current_save_slot = []
        self.macros = []
        self.current_macro = []
        self.settings = {}
        self.game_controls = {}
        self.init_ui()

        # Here must be an attempt to get things from outer file.
        # self.read_settings()

        if not self.save_file_location:
            self.save_file_location = self.calculated_save_file_path()

        self.after_save_file_location_changing()

        self.show()

    def init_ui(self):
        """

        """
        self.setupUi(self)

        self.center_window()
        self.button_OpenSaveFile.clicked.connect(self.open_save_file)

        # Macros table.
        self.tableWidget_Macros.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_Macros.setColumnHidden(0, True) # Hide ID column


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

    @staticmethod
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


def start_application():
    """

    """

    app = QApplication(sys.argv)

    window = MainWindow()
    window.setWindowTitle('ER - Melina Fingers')
    sys.exit(app.exec_())


if __name__ == '__main__':

    start_application()

    # savefile.get_controls()

    # keyboard.add_hotkey('ctrl+p', lambda: print('You pressed p'))
    # keyboard.add_hotkey('o', lambda _: sort_all_lists())
    # # For catching keyboard presses.
    # with Listener(on_press=on_press) as listener:
    #     listener.join()
