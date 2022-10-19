import os
import sys
import savefile
from mainWindow import Ui_MainWindow
from PyQt5.QtWidgets import *
from pathlib import Path
from macro import Macro, built_in_macros, available_hotkey_buttons
from savefile import SaveSlot
import keyboard

def available_game_control_buttons() -> tuple:
    """
    List of keyboard buttons that can be used to assign in Elden Ring.
    """

    return (
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "0",
        "Num0",
        "Num1",
        "Num2",
        "Num3",
        "Num4",
        "Num5",
        "Num6",
        "Num7",
        "Num8",
        "Num9",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "Tab",
        "Space",
        "Backspace",
        "Enter",
        "Home",
        "PageUp",
        "End",
        "PageDown",
        "Insert",
        "Delete",
        "Ctrl",
        "Shift",
        "Alt"
    )

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):

        super(MainWindow, self).__init__(*args, **kwargs)

        self.save_file_location: str = ''
        self.save_slots: list = []
        self.current_save_slot: SaveSlot = SaveSlot()
        self.current_macro: Macro = Macro()
        self.settings: dict = {
            '': ''
        }
        self.standard_pause_time: int = 0
        self.interrupt_hotkey: str = ''
        self.interrupt_hotkey_ctrl: bool = False
        self.interrupt_hotkey_shift: bool = False
        self.interrupt_hotkey_alt: bool = False

        self.init_ui()

        if not self.save_file_location:
            self.save_file_location = self.calculated_save_file_path()

        self.read_game_controls_from_save_file()
        self.read_all_equipment()
        self.read_settings()
        self.set_standard_settings()
        self.hook_hotkeys()
        self.add_introductory_macros()
        self.set_macros_settings()
        self.fill_builtin_macros()

        self.fill_save_slots()
        self.comboBox_SaveSlots_Refresh()
        self.tableWidget_Macros_Refresh()
        self.MacroArea_Refresh()
        self.stackedWidget_Pages_RefreshAll()
        self.stackedWidget_Pages_SetPage()

        self.show()

    def fill_builtin_macros(self) -> None:
        """
        Fills a table on 'Built-in' page.
        """

        # Clearing table.
        while self.tableWidget_BuiltInMacros.rowCount():
            self.tableWidget_BuiltInMacros.removeRow(0)

        for i, builtin_macro in enumerate(built_in_macros()):
            self.tableWidget_BuiltInMacros.insertRow(i)
            self.tableWidget_BuiltInMacros.setItem(i, 0, QTableWidgetItem(
                builtin_macro['name']))

    def add_introductory_macros(self) -> None:
        """
        Adds some macros for introducing to Melina's Fingers if there's no
        settings file yet.
        """

    def set_macros_settings(self) -> None:
        """
        Sets some setting to all macros in window.
        """

        interrupt_hotkey = self.interrupt_hotkey
        if self.interrupt_hotkey_alt:
            interrupt_hotkey = 'alt+' + interrupt_hotkey
        if self.interrupt_hotkey_shift:
            interrupt_hotkey = 'shift+' + interrupt_hotkey
        if self.interrupt_hotkey_ctrl:
            interrupt_hotkey = 'ctrl+' + interrupt_hotkey

        for macro in self.current_save_slot.macros:
            macro.pause_time = self.standard_pause_time
            macro.interrupted = False
            macro.interrupt_hotkey = interrupt_hotkey
            macro.save_slot = self.current_save_slot

    def set_standard_settings(self) -> None:
        """
        Set some setting to their standard values if it's not set yet via
        settings file on manually.
        """

        if self.interrupt_hotkey == '':
            self.interrupt_hotkey = 'Tab'

        if self.standard_pause_time == 0:
            self.standard_pause_time = 20


    def read_game_controls_from_save_file(self):
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
            self.current_save_slot.game_controls[key] = control_keys[key]

    def hook_hotkeys(self):
        """

        """

        # Try block, because 'Keyboard' clearing methods can call
        # an unexpected exception if there's no assigned hotkeys.
        try:
            keyboard.remove_all_hotkeys()
            keyboard._hotkeys.clear()
        except:
            pass

        # Hooking interrupt hotkey, that interrupts ongoing macro.


        for macro in self.current_save_slot.macros:

            hotkey_string = macro.hotkey_string()

            # Condition helps to correct a situation when several hotkeys
            # are assign to one key.
            if hotkey_string not in keyboard._hotkeys:
                keyboard.add_hotkey(hotkey_string,
                                    macro.execute,
                                    suppress=True,
                                    trigger_on_release=True)

    def read_all_equipment(self):
        """

        """

        if self.save_file_location == '' \
                or self.current_save_slot.id == 0:
            return

        result = savefile.get_all_equipment(self.save_file_location,
                                            self.current_save_slot.id)

        # TODO: Распределить по атрибутам окна

    def init_ui(self):
        """

        """
        self.setupUi(self)  # automaticly generated code

        self.setFixedSize(1600, 890)
        self.setWindowTitle('ER - Melina\'s Fingers')
        self.button_OpenSaveFile.clicked.connect(self.OpenSaveFile_Click)
        self.button_SaveSettings.clicked.connect(self.save_settings)
        self.button_AddMacros.clicked.connect(self.AddMacros_Click)
        self.button_Settings.clicked.connect(self.Settings_Click)
        self.comboBox_SaveSlots.activated.connect(self.comboBox_SaveSlots_OnChange)
        self.tableWidget_Macros.cellClicked.connect(self.tableWidget_Macros_Clicked)
        self.lineEdit_MacroName.editingFinished.connect(self.lineEdit_MacroName_OnChange)
        self.comboBox_MacroType.activated.connect(self.comboBox_MacroType_OnChange)
        self.button_DeleteMacros.clicked.connect(self.DeleteMacros_Click)
        self.comboBox_MacroKey.activated.connect(self.comboBox_MacroKey_OnChange)
        self.checkBox_MacroKeyCtrl.clicked.connect(self.MacroKeyCtrl_Click)
        self.checkBox_MacroKeyShift.clicked.connect(self.MacroKeyShift_Click)
        self.checkBox_MacroKeyAlt.clicked.connect(self.MacroKeyAlt_Click)
        for key in available_hotkey_buttons():
            self.comboBox_MacroKey.addItem(key)
            self.comboBox_InterruptHotkey.addItem(key)

        # Page "Built-in"
        self.tableWidget_BuiltInMacros.cellClicked.connect(self.tableWidget_BuiltInMacros_OnChange)

        # Page "DIY"
        self.textEdit_DIY.textChanged.connect(self.textEdit_DIY_OnChange)

        # Page "Settings"
        self.comboBox_InterruptHotkey.activated.connect(self.comboBox_InterruptKey_OnChange)
        self.checkBox_InterruptKeyCtrl.clicked.connect(self.InterruptKeyCtrl_Click)
        self.checkBox_InterruptKeyShift.clicked.connect(self.InterruptKeyShift_Click)
        self.checkBox_InterruptKeyAlt.clicked.connect(self.InterruptKeyAlt_Click)

        self.comboBox_ControlKeyJump.activated.connect(self.ControlKeys_OnChange)
        self.comboBox_ControlKeyRoll.activated.connect(self.ControlKeys_OnChange)
        self.comboBox_ControlKeyCrouch.activated.connect(self.ControlKeys_OnChange)
        self.comboBox_ControlKeyResetCamera.activated.connect(self.ControlKeys_OnChange)
        self.comboBox_ControlKeyAttack.activated.connect(self.ControlKeys_OnChange)
        self.comboBox_ControlKeyStrongAttack.activated.connect(self.ControlKeys_OnChange)
        self.comboBox_ControlKeySkill.activated.connect(self.ControlKeys_OnChange)
        self.comboBox_ControlKeySwitchItem.activated.connect(self.ControlKeys_OnChange)
        self.comboBox_ControlKeySwitchSpell.activated.connect(self.ControlKeys_OnChange)
        self.comboBox_ControlKeyGuard.activated.connect(self.ControlKeys_OnChange)
        self.comboBox_ControlKeyUseItem.activated.connect(self.ControlKeys_OnChange)
        self.comboBox_ControlKeyUse.activated.connect(self.ControlKeys_OnChange)

        for key in available_game_control_buttons():
            self.comboBox_ControlKeyJump.addItem(key)
            self.comboBox_ControlKeyRoll.addItem(key)
            self.comboBox_ControlKeyCrouch.addItem(key)
            self.comboBox_ControlKeyResetCamera.addItem(key)
            self.comboBox_ControlKeyAttack.addItem(key)
            self.comboBox_ControlKeyStrongAttack.addItem(key)
            self.comboBox_ControlKeySkill.addItem(key)
            self.comboBox_ControlKeySwitchItem.addItem(key)
            self.comboBox_ControlKeySwitchSpell.addItem(key)
            self.comboBox_ControlKeyGuard.addItem(key)
            self.comboBox_ControlKeyUseItem.addItem(key)
            self.comboBox_ControlKeyUse.addItem(key)

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
        self.current_save_slot = next((x for x in self.save_slots if x.id == slot_id), SaveSlot())
        self.current_macro = Macro()

        self.read_all_equipment()
        self.hook_hotkeys()

        self.tableWidget_Macros_Refresh()
        self.MacroArea_Refresh()
        self.stackedWidget_Pages_RefreshAll()
        self.stackedWidget_Pages_SetPage()

    def tableWidget_Macros_Clicked(self, index):
        """

        :return:
        """
        macro_id = int(self.tableWidget_Macros.item(index, 0).text())
        self.current_macro = next((x for x in self.current_save_slot.macros if x.id == macro_id), Macro())

        self.set_macros_settings()

        self.MacroArea_Refresh()
        self.stackedWidget_Pages_SetPage()
        self.stackedWidget_Pages_RefreshAll()

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

        # TODO: Не забыть стандартные значения забить при выборе типа
        # Set standard values.
        if self.current_macro.type == 'Equipment':
            pass

        if self.current_macro.type == 'Magic':
            pass

        if self.current_macro.type == 'Built-in' \
                and self.current_macro.settings['built-in']['macro_name'] == '':
            self.current_macro.settings['built-in']['macro_name'] = built_in_macros()[0]['name']

        self.hook_hotkeys()
        self.stackedWidget_Pages_SetPage()
        self.stackedWidget_Pages_RefreshAll()



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
            self.current_macro = Macro()
            self.fill_save_slots()
            self.read_game_controls_from_save_file()
            self.read_all_equipment()
            self.hook_hotkeys()
            self.set_macros_settings()

            self.comboBox_SaveSlots_Refresh()
            self.tableWidget_Macros_Refresh()
            self.MacroArea_Refresh()
            self.stackedWidget_Pages_SetPage()
            self.stackedWidget_Pages_RefreshAll()

    def Settings_Click(self):
        """

        :return:
        """
        if self.stackedWidget_Pages.currentIndex() != 5:
            self.stackedWidget_Pages.setCurrentIndex(5)
        else:
            self.stackedWidget_Pages_SetPage()

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
        self.set_macros_settings()

        self.tableWidget_Macros_Refresh()
        self.MacroArea_Refresh()
        self.stackedWidget_Pages_SetPage()
        self.stackedWidget_Pages_RefreshAll()

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

    def comboBox_InterruptKey_OnChange(self):
        """

        """

        current_text = self.comboBox_InterruptHotkey.currentText()
        self.interrupt_hotkey = current_text

        self.set_macros_settings()

    def InterruptKeyCtrl_Click(self):
        """

        """

        checked = self.checkBox_InterruptKeyCtrl.isChecked()
        self.interrupt_hotkey_ctrl = checked
        self.set_macros_settings()

    def InterruptKeyShift_Click(self):
        """

        """
        checked = self.checkBox_InterruptKeyShift.isChecked()
        self.interrupt_hotkey_shift = checked
        self.set_macros_settings()

    def InterruptKeyAlt_Click(self):
        """

        """

        checked = self.checkBox_InterruptKeyAlt.isChecked()
        self.interrupt_hotkey_alt = checked
        self.set_macros_settings()

    def DeleteMacros_Click(self):
        """

        :return:
        """

        self.current_save_slot.macros.remove(self.current_macro)
        self.current_macro = Macro()
        self.hook_hotkeys()
        self.set_macros_settings()

        self.tableWidget_Macros_Refresh()
        self.MacroArea_Refresh()
        self.stackedWidget_Pages_SetPage()

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

    def stackedWidget_Pages_SetPage(self) -> None:
        """

        """
        current_type = self.current_macro.type
        if self.current_macro.type:
            types_indexes = {
                'Equipment': 1,
                'Magic': 2,
                'Built-in': 3,
                'DIY': 4
            }

            self.stackedWidget_Pages.setCurrentIndex(types_indexes[current_type])
        else:
            self.stackedWidget_Pages.setCurrentIndex(0)

    def stackedWidget_Pages_RefreshAll(self) -> None:
        """

        """
        self.stackedWidget_Pages_Refresh_Equipment()
        self.stackedWidget_Pages_Refresh_Magic()
        self.stackedWidget_Pages_Refresh_Builtin()
        self.stackedWidget_Pages_Refresh_DIY()
        self.stackedWidget_Pages_Refresh_Settings()
        self.stackedWidget_Pages_Refresh_Multiplayer()

    def stackedWidget_Pages_Refresh_Equipment(self) -> None:
        """

        """

        pass

    def stackedWidget_Pages_Refresh_Magic(self) -> None:
        """

        """

        pass

    def stackedWidget_Pages_Refresh_Builtin(self) -> None:
        """

        """

        current_builtin_macro_name = self.current_macro.settings['built-in']['macro_name']

        # Comment label.
        if current_builtin_macro_name:
            builtin_macro = next((x for x in built_in_macros() if x['name'] == current_builtin_macro_name), None)
            if builtin_macro is not None:
                self.label_BuiltInMacroComment.setText(builtin_macro['comment'])
        else:
            self.label_BuiltInMacroComment.setText('')

        # Table.
        self.tableWidget_BuiltInMacros.clearSelection()
        if current_builtin_macro_name:
            for i, item in enumerate(built_in_macros()):
                if item['name'] == current_builtin_macro_name:
                    self.tableWidget_BuiltInMacros.selectRow(i)
                    break


    def stackedWidget_Pages_Refresh_DIY(self) -> None:
        """

        """

        self.textEdit_DIY.setText(self.current_macro.settings['diy']['macro'])

    def stackedWidget_Pages_Refresh_Settings(self) -> None:
        """

        """

        # Interrupt hotkey.
        self.comboBox_InterruptHotkey.setCurrentText(self.interrupt_hotkey)
        self.checkBox_InterruptKeyCtrl.setChecked(self.interrupt_hotkey_ctrl)
        self.checkBox_InterruptKeyShift.setChecked(self.interrupt_hotkey_shift)
        self.checkBox_InterruptKeyAlt.setChecked(self.interrupt_hotkey_alt)

        # Controls in Elden Ring.
        self.comboBox_ControlKeyRoll.setCurrentText(self.current_save_slot.game_controls['roll'])
        self.comboBox_ControlKeyJump.setCurrentText(self.current_save_slot.game_controls['jump'])
        self.comboBox_ControlKeyCrouch.setCurrentText(self.current_save_slot.game_controls['crouch'])
        self.comboBox_ControlKeyResetCamera.setCurrentText(self.current_save_slot.game_controls['reset_camera'])
        self.comboBox_ControlKeyAttack.setCurrentText(self.current_save_slot.game_controls['attack'])
        self.comboBox_ControlKeyStrongAttack.setCurrentText(self.current_save_slot.game_controls['strong_attack'])
        self.comboBox_ControlKeySkill.setCurrentText(self.current_save_slot.game_controls['skill'])
        self.comboBox_ControlKeySwitchItem.setCurrentText(self.current_save_slot.game_controls['switch_item'])
        self.comboBox_ControlKeySwitchSpell.setCurrentText(self.current_save_slot.game_controls['switch_spell'])
        self.comboBox_ControlKeyGuard.setCurrentText(self.current_save_slot.game_controls['guard'])
        self.comboBox_ControlKeyUseItem.setCurrentText(self.current_save_slot.game_controls['use_item'])
        self.comboBox_ControlKeyUse.setCurrentText(self.current_save_slot.game_controls['event_action'])

        # Standard pause time.
        self.spinBox_StandardPauseTime.setValue(self.standard_pause_time)


    def stackedWidget_Pages_Refresh_Multiplayer(self) -> None:
        """

        """

        pass

    def tableWidget_BuiltInMacros_OnChange(self) -> None:
        """

        """

        items = self.tableWidget_BuiltInMacros.selectedItems()
        if len(items):
            self.current_macro.settings['built-in']['macro_name'] = items[0].text()
            self.stackedWidget_Pages_Refresh_Builtin()

    def ControlKeys_OnChange(self):
        """

        """

        self.current_save_slot.game_controls['roll'] = self.comboBox_ControlKeyRoll.currentText().lower()
        self.current_save_slot.game_controls['jump'] = self.comboBox_ControlKeyJump.currentText().lower()
        self.current_save_slot.game_controls['crouch'] = self.comboBox_ControlKeyCrouch.currentText().lower()
        self.current_save_slot.game_controls['reset_camera'] = self.comboBox_ControlKeyResetCamera.currentText().lower()
        self.current_save_slot.game_controls['attack'] = self.comboBox_ControlKeyAttack.currentText().lower()
        self.current_save_slot.game_controls['strong_attack'] = self.comboBox_ControlKeyStrongAttack.currentText().lower()
        self.current_save_slot.game_controls['skill'] = self.comboBox_ControlKeySkill.currentText().lower()
        self.current_save_slot.game_controls['switch_item'] = self.comboBox_ControlKeySwitchItem.currentText().lower()
        self.current_save_slot.game_controls['switch_spell'] = self.comboBox_ControlKeySwitchSpell.currentText().lower()
        self.current_save_slot.game_controls['guard'] = self.comboBox_ControlKeyGuard.currentText().lower()
        self.current_save_slot.game_controls['use_item'] = self.comboBox_ControlKeyUseItem.currentText().lower()
        self.current_save_slot.game_controls['event_action'] = self.comboBox_ControlKeyUse.currentText().lower()

        self.set_macros_settings()

    def textEdit_DIY_OnChange(self):
        """

        """

        self.current_macro.settings['diy']['macro'] = self.textEdit_DIY.toPlainText()

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
