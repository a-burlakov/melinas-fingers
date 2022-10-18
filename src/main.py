import os
import sys
import savefile
from win32gui import GetWindowText, GetForegroundWindow
from mainWindow import Ui_MainWindow
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pathlib import Path
from macro import Macro

import keyboard


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
        # ("LShift", "Shift (left)"),
        # ("RShift", "Shift (right)"),
        # ("LCtrl", "Control (left)"),
        # ("RCtrl", "Control (right)"),
        ("Space", "Space"),
        ("Backspace", "Backspace"),
        ("Enter", "Enter (main)"),
        # ("Enter (num)", "Enter (numpad)"),
        # ("LAlt", "Alt (left)"),
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
        self.macros: list = []
        self.weapon_list: list = []
        self.armor_head_list: list = []
        self.armor_torso_list: list = []
        self.armor_hands_list: list = []
        self.armor_legs_list: list = []
        self.talisman_list: list = []
        self.spell_list: list = []
        # self.item_list: list = []

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):

        super(MainWindow, self).__init__(*args, **kwargs)

        self.save_file_location: str = ''
        self.save_slots: list = []
        self.current_save_slot: SaveSlot = SaveSlot()
        self.current_macro: Macro = Macro()
        self.settings: dict = {}
        self.game_controls: dict = {
            'roll': '',
            'jump': '',
            'crouch': '',
            'reset_camera': '',
            'switch_spell': '',
            'switch_item': '',
            'attack': '',
            'strong_attack': '',
            'guard': '',
            'skill': '',
            'use_item': '',
            'use': ''
        }

        self.init_ui()

        # TODO: add introductory macros

        if not self.save_file_location:
            self.save_file_location = self.calculated_save_file_path()

        self.read_game_controls()
        self.read_all_equipment()
        self.read_settings()
        self.hook_hotkeys()

        self.fill_save_slots()
        self.comboBox_SaveSlots_Refresh()
        self.tableWidget_Macros_Refresh()
        self.MacroArea_Refresh()
        self.tabWidget_Pages_Refresh()

        self.show()

    def read_game_controls(self):
        """

        """

        if self.save_file_location == '':
            return

        slot_data = savefile.get_slot_data(self.save_file_location)

        control_keys = savefile.control_keys_ranges()
        for key, value in control_keys.items():
            hex_string = slot_data[value:value + 1]
            control_keys[key] = int(hex_string.hex(), 16)
            control_keys[key] = savefile.control_keys_values().get(
                control_keys[key], '')
            self.game_controls[key] = control_keys[key]

    def hook_hotkeys(self):
        """

        """
        try:
            keyboard.remove_all_hotkeys()
        except:
            pass
        # if hasattr(keyboard, 'hotkeys') and len() > 0:
        #     keyboard.unhook_all_hotkeys()
        #     print('hotkeys removed')

        for macro in self.current_save_slot.macros:
            hotkey_string = macro.hotkey_string()
            keyboard.add_hotkey(hotkey_string, lambda: self.macro_press_hotkey(macro), suppress=True, trigger_on_release=True)
            print(len(keyboard._hotkeys))

    def macro_press_hotkey(self, macro: Macro):
        """
        execute macro
        """

        print(macro)
        # current_window_text: str = (GetWindowText(GetForegroundWindow()))
        # if 'elden' not in current_window_text.lower() \
        #         and 'melina' not in current_window_text.lower():
        #     return
        #
        # # TODO: Если поймали кнопку, отвечающую за блок алгоритма, то нажимаем ее. Возможно, установить булево значение какое-нибудь в макрос.
        #
        # macro.execute()

    def read_all_equipment(self):
        """

        """

        if self.save_file_location == ''\
                or self.current_save_slot.id == 0:
            return

        result = savefile.get_all_equipment(self.save_file_location,
                                            self.current_save_slot.id)

        pass

    def init_ui(self):
        """

        """
        self.setupUi(self)

        self.center_window()
        self.setWindowTitle('ER - Melina\'s Fingers')
        self.button_OpenSaveFile.clicked.connect(self.OpenSaveFile_Click)
        self.button_SaveSettings.clicked.connect(self.save_settings)
        self.button_AddMacros.clicked.connect(self.AddMacros_Click)
        self.comboBox_SaveSlots.activated.connect(self.comboBox_SaveSlots_OnChange)
        self.tableWidget_Macros.cellClicked.connect(self.tableWidget_Macros_Clicked)
        self.lineEdit_MacroName.editingFinished.connect(self.lineEdit_MacroName_OnChange)
        self.comboBox_MacroType.activated.connect(self.comboBox_MacroType_OnChange)
        self.comboBox_MacroKey.activated.connect(self.comboBox_MacroKey_OnChange)
        self.button_DeleteMacros.clicked.connect(self.DeleteMacros_Click)
        self.checkBox_MacroKeyCtrl.clicked.connect(self.MacroKeyCtrl_Click)
        self.checkBox_MacroKeyShift.clicked.connect(self.MacroKeyShift_Click)
        self.checkBox_MacroKeyAlt.clicked.connect(self.MacroKeyAlt_Click)
        for key in available_hotkey_buttons():
            self.comboBox_MacroKey.addItem(key[0])

        # Macros table.
        self.tableWidget_Macros.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_Macros.setColumnHidden(0, True)  # Hide ID column

    def save_settings(self):
        """

        """

        pass

    def read_settings(self):
        """

        """

        self.hook_hotkeys()

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
                self.comboBox_SaveSlots.addItem(
                    f'{save_slot.id}. {save_slot.name}')
        else:
            self.comboBox_SaveSlots.addItem('<Choose save file!>')

        self.comboBox_SaveSlots.setEnabled(len(self.save_slots) > 0)

    def comboBox_SaveSlots_OnChange(self):
        """

        """
        current_text = self.comboBox_SaveSlots.currentText()
        slot_id = int(current_text.split('.')[0])
        self.current_save_slot = next(
            x for x in self.save_slots if x.id == slot_id)
        self.current_macro = Macro()

        self.read_all_equipment()
        self.hook_hotkeys()
        self.tableWidget_Macros_Refresh()
        self.MacroArea_Refresh()
        self.tabWidget_Pages_Refresh()

    def tableWidget_Macros_Clicked(self, index):
        """

        :return:
        """
        macro_id = int(self.tableWidget_Macros.item(index, 0).text())
        self.current_macro = next(
            x for x in self.current_save_slot.macros if x.id == macro_id)

        self.MacroArea_Refresh()

    def tableWidget_Macros_Refresh(self):
        """

        :return:
        """

        self.button_AddMacros.setEnabled(len(self.save_slots) > 0)
        self.button_DeleteMacros.setEnabled(len(self.save_slots) > 0)

        # Clearing table.
        while self.tableWidget_Macros.rowCount():
            self.tableWidget_Macros.removeRow(0)

        for i, macro in enumerate(self.current_save_slot.macros):

            hotkey_list = []
            hotkey = ''
            if macro.hotkey:
                if macro.hotkey_ctrl:
                    hotkey_list.append('Ctrl')
                if macro.hotkey_shift:
                    hotkey_list.append('Shift')
                if macro.hotkey_alt:
                    hotkey_list.append('Alt')
                hotkey_list.append(macro.hotkey)
                hotkey = '+'.join(hotkey_list)

            self.tableWidget_Macros.insertRow(i)
            self.tableWidget_Macros.setItem(i, 0,
                                            QTableWidgetItem(str(macro.id)))
            self.tableWidget_Macros.setItem(i, 1, QTableWidgetItem(macro.name))
            self.tableWidget_Macros.setItem(i, 2, QTableWidgetItem(hotkey))

    def lineEdit_MacroName_OnChange(self):
        """

        """
        self.current_macro.name = self.lineEdit_MacroName.text()
        self.tableWidget_Macros_Refresh()

    def comboBox_MacroType_OnChange(self):
        """

        """
        self.current_macro.type = self.comboBox_MacroType.currentText()
        self.hook_hotkeys()
        self.tabWidget_Pages_Refresh()

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
            self.read_game_controls()
            self.fill_save_slots()
            self.read_all_equipment()
            self.hook_hotkeys()

            self.comboBox_SaveSlots_Refresh()
            self.tableWidget_Macros_Refresh()
            self.MacroArea_Refresh()
            self.tabWidget_Pages_Refresh()

    def AddMacros_Click(self):
        """

        :return:
        """

        new_macro = Macro()
        new_macro.name = '< hotkey name >'
        new_macro.id = self.get_new_macro_id()
        new_macro.type = 'Equipment'
        new_macro.hotkey = 'F1'

        self.current_save_slot.macros.append(new_macro)
        self.current_macro = new_macro

        self.hook_hotkeys()
        self.tableWidget_Macros_Refresh()
        self.MacroArea_Refresh()
        self.tabWidget_Pages_Refresh()

    def comboBox_MacroKey_OnChange(self):
        """

        """

        current_text = self.comboBox_MacroKey.currentText()
        self.current_macro.hotkey = current_text

        self.hook_hotkeys()
        self.tableWidget_Macros_Refresh()

    def MacroKeyCtrl_Click(self):
        """

        """


        checked = self.checkBox_MacroKeyCtrl.isChecked()
        self.current_macro.hotkey_ctrl = checked
        self.hook_hotkeys()
        self.tableWidget_Macros_Refresh()

    def MacroKeyShift_Click(self):
        """

        """
        checked = self.checkBox_MacroKeyShift.isChecked()
        self.current_macro.hotkey_shift = checked
        self.hook_hotkeys()
        self.tableWidget_Macros_Refresh()

    def MacroKeyAlt_Click(self):
        """

        """

        checked = self.checkBox_MacroKeyAlt.isChecked()
        self.current_macro.hotkey_alt = checked
        self.hook_hotkeys()
        self.tableWidget_Macros_Refresh()

    def DeleteMacros_Click(self):
        """

        :return:
        """

        self.current_save_slot.macros.remove(self.current_macro)
        self.current_macro = Macro()

        self.tableWidget_Macros_Refresh()
        self.MacroArea_Refresh()
        self.tabWidget_Pages_Refresh()

    def get_new_macro_id(self):
        """

        :return:
        """

        if len(self.current_save_slot.macros):
            max_id = max(self.current_save_slot.macros,
                         key=lambda macro: macro.id).id
            new_id = max_id + 1
        else:
            new_id = new_id = self.current_save_slot.id * 1000 + 1

        return new_id

    def MacroArea_Refresh(self):
        """

        :return:
        """

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
            self.comboBox_MacroType.setCurrentText(self.current_macro.type)
            self.comboBox_MacroKey.setCurrentText(self.current_macro.hotkey)
            self.checkBox_MacroKeyShift.setChecked(
                self.current_macro.hotkey_shift)
            self.checkBox_MacroKeyAlt.setChecked(self.current_macro.hotkey_alt)
            self.checkBox_MacroKeyCtrl.setChecked(
                self.current_macro.hotkey_ctrl)
        else:
            self.lineEdit_MacroName.setText('')
            self.comboBox_MacroType.setCurrentIndex(0)
            self.comboBox_MacroKey.setCurrentIndex(0)
            self.checkBox_MacroKeyShift.setChecked(False)
            self.checkBox_MacroKeyAlt.setChecked(False)
            self.checkBox_MacroKeyCtrl.setChecked(False)

    def tabWidget_Pages_Refresh(self):
        """

        :return:
        """
        current_type = self.current_macro.type
        if self.current_macro.type:
            types_indexes = {
                'Equipment': 0,
                'Magic': 1,
                'Items': 2,
                'Built-in': 3,
                'DIY': 4
            }

            self.tabWidget_Pages.setCurrentIndex(types_indexes[current_type])
        else:
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

    sys.exit(app.exec_())


if __name__ == '__main__':

    start_application()
    # keyboard.add_hotkey('o', lambda _: sort_all_lists())
    # # For catching keyboard presses.
    # with Listener(on_press=on_press) as listener:
    #     listener.join()
