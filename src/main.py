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
        self.id: int = 0
        self.name: str = ''
        self.weapon_list: list = []
        self.armor_head_list: list = []
        self.armor_torso_list: list = []
        self.armor_hands_list: list = []
        self.armor_legs_list: list = []
        self.talisman_list: list = []
        self.spell_list: list = []
        self.item_list: list = []


class Macro:
    """

    """

    def __init__(self):
        self.id: int = 0
        self.name: str = ''
        self.type: str = ''
        self.hotkey: str = ''
        self.hotkey_ctrl: bool = False
        self.hotkey_shift: bool = False
        self.hotkey_alt: bool = False


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):

        super(MainWindow, self).__init__(*args, **kwargs)

        self.save_file_location: str = ''
        self.save_slots: list = []
        self.current_save_slot: SaveSlot = SaveSlot()
        self.macros: list = []
        self.current_macro: Macro = Macro()
        self.settings: dict = {}
        self.game_controls: dict = {}

        self.init_ui()

        # Here must be an attempt to get things from outer file.
        # self.read_settings()

        if not self.save_file_location:
            self.save_file_location = self.calculated_save_file_path()

        self.fill_save_slots()
        self.comboBox_SaveSlots_Refresh()
        self.tableWidget_Macros_Refresh()
        self.MacroArea_Refresh()
        self.tabWidget_Pages_Refresh()

        self.show()

    def init_ui(self):
        """

        """
        self.setupUi(self)

        self.center_window()
        self.button_OpenSaveFile.clicked.connect(self.OpenSaveFile_Click)
        self.button_AddMacros.clicked.connect(self.AddMacros_Click)
        self.button_DeleteMacros.clicked.connect(self.DeleteMacros_Click)
        self.comboBox_SaveSlots.activated.connect(self.comboBox_SaveSlots_OnChange)
        self.tableWidget_Macros.cellClicked.connect(self.tableWidget_Macros_Clicked)
        self.lineEdit_MacroName.editingFinished.connect(self.lineEdit_MacroName_OnChange)
        # Macros table.
        self.tableWidget_Macros.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_Macros.setColumnHidden(0, True)  # Hide ID column

    def fill_save_slots(self):
        """

        """

        self.save_slots.clear()
        if self.save_file_location:
            names = savefile.get_slot_names(self.save_file_location)
            for i, name in enumerate(names, 1):
                if name:
                    save_slot = SaveSlot()
                    save_slot.id = i
                    save_slot.name = name
                    self.save_slots.append(save_slot)
            self.current_save_slot = self.save_slots[0]

    def comboBox_SaveSlots_Refresh(self):
        """

        """

        # Init save-slots.
        self.comboBox_SaveSlots.clear()
        if self.save_slots:
            for save_slot in self.save_slots:
                    self.comboBox_SaveSlots.addItem(f'{save_slot.id}. {save_slot.name}')
        else:
            self.comboBox_SaveSlots.addItem('<Choose save file!>')

        self.comboBox_SaveSlots.setEnabled(len(self.save_slots) > 0)

    def comboBox_SaveSlots_OnChange(self):
        """

        """
        print('wow')

    def tableWidget_Macros_Clicked(self, index):
        """

        :return:
        """
        macro_id = int(self.tableWidget_Macros.item(index, 0).text())
        self.current_macro = next(x for x in self.macros if x.id == macro_id)

        self.MacroArea_Refresh()

    def lineEdit_MacroName_OnChange(self):
        """

        """
        self.current_macro.name = self.lineEdit_MacroName.text()
        self.tableWidget_Macros_Refresh()

    def OpenSaveFile_Click(self):
        """

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
            self.fill_save_slots()
            self.comboBox_SaveSlots_Refresh()
            self.tableWidget_Macros_Refresh()
            self.MacroArea_Refresh()
            self.tabWidget_Pages_Refresh()

    def AddMacros_Click(self):
        """

        :return:
        """

        new_macro = Macro()
        new_macro.name = '<hotkey name>'
        new_macro.id = self.get_new_macro_id()

        self.macros.append(new_macro)
        self.current_macro = new_macro

        self.tableWidget_Macros_Refresh()
        self.MacroArea_Refresh()
        self.tabWidget_Pages_Refresh()

    def DeleteMacros_Click(self):
        """

        :return:
        """


        self.macros.remove(self.current_macro)
        self.current_macro = Macro()

        self.tableWidget_Macros_Refresh()
        self.MacroArea_Refresh()
        self.tabWidget_Pages_Refresh()

    def get_new_macro_id(self):
        """

        :return:
        """

        if len(self.macros):
            max_id = max(self.macros, key=lambda macro: macro.id).id
            new_id = max_id + 1
        else:
            new_id = new_id = self.current_save_slot.id * 1000 + 1

        return new_id

    def tableWidget_Macros_Refresh(self):
        """

        :return:
        """

        self.button_AddMacros.setEnabled(len(self.save_slots) > 0)
        self.button_DeleteMacros.setEnabled(len(self.save_slots) > 0)

        # Clearing table.
        while self.tableWidget_Macros.rowCount():
            self.tableWidget_Macros.removeRow(0)

        for i, macro in enumerate(self.macros):
            self.tableWidget_Macros.insertRow(i)
            self.tableWidget_Macros.setItem(i, 0, QTableWidgetItem(str(macro.id)))
            self.tableWidget_Macros.setItem(i, 1, QTableWidgetItem(macro.name))
            self.tableWidget_Macros.setItem(i, 2, QTableWidgetItem(macro.hotkey))

    def MacroArea_Refresh(self):
        """

        :return:
        """
        # TODO: обнулять значения всех полей
        macro_is_chosen = (self.current_macro.id > 0)
        self.lineEdit_MacroName.setEnabled(macro_is_chosen)
        self.button_DeleteMacros.setEnabled(macro_is_chosen)
        self.comboBox_MacroKey.setEnabled(macro_is_chosen)
        self.comboBox_MacroType.setEnabled(macro_is_chosen)
        self.checkBox_MacroKeyAlt.setEnabled(macro_is_chosen)
        self.checkBox_MacroKeyCtrl.setEnabled(macro_is_chosen)
        self.checkBox_MacroKeyShift.setEnabled(macro_is_chosen)

        if macro_is_chosen:
            self.lineEdit_MacroName.setText(self.current_macro.name)

    def tabWidget_Pages_Refresh(self):
        """

        :return:
        """
        pass

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
