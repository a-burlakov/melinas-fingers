import sys
import os
from pathlib import Path
from mainWindow import Ui_MainWindow
from PyQt5.QtWidgets import *
from macro import Macro, built_in_macros, available_hotkey_buttons
from savefile import SaveFile, SaveSlot
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

        self.savefile: SaveFile = SaveFile('')
        self.current_saveslot: SaveSlot = SaveSlot()
        self.current_macro: Macro = Macro()
        self.settings: dict = {'': ''}
        self.standard_pause_time: int = 0
        self.interrupt_hotkey: str = ''
        self.interrupt_hotkey_ctrl: bool = False
        self.interrupt_hotkey_shift: bool = False
        self.interrupt_hotkey_alt: bool = False

        self.init_ui()

        self.read_settings()

        # TODO: слишком сложно тут, надо все это выровнять в одну функцию, которую вызывать и из открытия сейва вручную
        if not self.savefile.location:
            self.savefile.calculate_savefile_location()
            if self.savefile.location:
                self.savefile.fill_saveslots()
                self.savefile.read_game_controls()
                if self.savefile.saveslots:
                    self.current_saveslot = self.savefile.saveslots[0]
                    self.current_saveslot.get_equipment()
                else:
                    self.current_saveslot = SaveSlot()
                self.current_macro = Macro()
                self.set_macros_settings_from_window()

        self.add_introductory_macros()
        self.set_macros_settings_from_window()
        self.fill_builtin_macros()
        self.AvailableSpells_RefillTable()
        self.refresh_all()

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

    def set_macros_settings_from_window(self) -> None:
        """
        Sets macros settings with values from the window to all macros.
        """

        interrupt_hotkey = self.interrupt_hotkey
        if self.interrupt_hotkey_alt:
            interrupt_hotkey = 'alt+' + interrupt_hotkey
        if self.interrupt_hotkey_shift:
            interrupt_hotkey = 'shift+' + interrupt_hotkey
        if self.interrupt_hotkey_ctrl:
            interrupt_hotkey = 'ctrl+' + interrupt_hotkey

        for macro in self.current_saveslot.macros:
            macro.pause_time = self.standard_pause_time
            macro.interrupted = False
            macro.interrupt_hotkey = interrupt_hotkey
            macro.saveslot = self.current_saveslot

    def hook_hotkeys(self):
        """

        """

        # Try block, because 'Keyboard' clearing methods can call
        # an unexpected exception if there's no assigned hotkeys.
        try:
            keyboard.remove_all_hotkeys()
            # keyboard._hotkeys.clear()
        except:
            pass

        for macro in self.current_saveslot.macros:

            hotkey_string = macro.hotkey_string()

            if not hotkey_string:
                continue

            # Condition helps to correct a situation when several hotkeys
            # are assign to one key.
            if hotkey_string not in keyboard._hotkeys:
                for move_key in ['', 'w+', 'a+', 's+', 'd+', 'w+a+', 'w+d+', 'd+s+', 'a+s+']:
                    keyboard.add_hotkey(move_key + hotkey_string,
                                        macro.execute,
                                        suppress=True,
                                        trigger_on_release=True)


    def init_ui(self):
        """

        """
        self.setupUi(self)  # automaticly generated code

        self.setFixedSize(1600, 890)
        self.setWindowTitle('ER - Melina\'s Fingers')
        self.button_OpenSaveFile.clicked.connect(self.OpenSaveFile_Click)
        self.button_SaveSettings.clicked.connect(self.save_settings)
        self.button_AddMacros.clicked.connect(self.AddMacro_Click)
        self.button_Settings.clicked.connect(self.Settings_Click)
        self.comboBox_SaveSlots.activated.connect(self.SaveSlots_OnChange)

        self.lineEdit_MacroName.editingFinished.connect(self.lineEdit_MacroName_OnChange)
        self.comboBox_MacroType.activated.connect(self.MacroType_OnChange)
        self.button_DeleteMacros.clicked.connect(self.DeleteMacros_Click)
        self.comboBox_MacroKey.activated.connect(self.MacroKey_OnChange)
        self.checkBox_MacroKeyCtrl.clicked.connect(self.MacroKeyCtrl_Click)
        self.checkBox_MacroKeyShift.clicked.connect(self.MacroKeyShift_Click)
        self.checkBox_MacroKeyAlt.clicked.connect(self.MacroKeyAlt_Click)
        for key in available_hotkey_buttons():
            self.comboBox_MacroKey.addItem(key)
            self.comboBox_InterruptHotkey.addItem(key)

        # Macros table.
        self.tableWidget_Macros.cellClicked.connect(self.tableWidget_Macros_Clicked)
        self.tableWidget_Macros.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_Macros.setColumnHidden(0, True)  # Hide ID column

        # Page "Equipment"

        # Page "Magic"
        self.tableWidget_AvaiableMagic.cellClicked.connect(self.AvaiableMagic_OnChange)
        self.tableWidget_AvaiableMagic.setEditTriggers(QTableWidget.NoEditTriggers)
        self.checkBox_MagicInstantUseLeftHand.clicked.connect(self.MagicInstantUseLeftHandCheck_OnChange)
        self.checkBox_MagicInstantUseRightHand.clicked.connect(self.MagicInstantUseRightHandCheck_OnChange)

        # Page "Built-in"
        self.tableWidget_BuiltInMacros.cellClicked.connect(self.BuiltInMacros_OnChange)
        self.tableWidget_BuiltInMacros.setEditTriggers(QTableWidget.NoEditTriggers)

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

    def save_settings(self):
        """

        """

        pass

    def read_settings(self):
        """

        """

        # Reading file.

        self.set_standard_settings()

    def set_standard_settings(self) -> None:
        """
        Set some settings to their standard values if it's not set yet via
        settings file on manually.
        """

        if self.interrupt_hotkey == '':
            self.interrupt_hotkey = 'Backspace'

        if self.standard_pause_time == 0:
            self.standard_pause_time = 20

    def SaveSlotsComboBox_Refresh(self):
        """
        Refresh the combobox for saveslot choosing.
        """

        saveslots = self.savefile.saveslots
        self.comboBox_SaveSlots.clear()
        if saveslots:
            for saveslot in saveslots:
                self.comboBox_SaveSlots.addItem(
                    f'{saveslot.number}. {saveslot.name}')
            self.comboBox_SaveSlots.setEnabled(True)
            self.comboBox_SaveSlots.setCurrentIndex(self.current_saveslot.number - 1)
        else:
            self.comboBox_SaveSlots.addItem('<Choose save file!>')
            self.comboBox_SaveSlots.setEnabled(False)

    def SaveSlots_OnChange(self):
        """
        Makes actions after choosing a saveslot in combobox.
        """
        current_text = self.comboBox_SaveSlots.currentText()
        slot_number = int(current_text.split('.')[0])
        self.current_saveslot = next((x for x in self.savefile.saveslots if x.number == slot_number), SaveSlot())
        self.current_saveslot.get_equipment()
        self.current_macro = Macro()

        self.AvailableSpells_RefillTable()
        self.refresh_all()

    def tableWidget_Macros_Clicked(self, index):
        """

        :return:
        """
        macro_id = int(self.tableWidget_Macros.item(index, 0).text())
        self.current_macro = next((x for x in self.current_saveslot.macros if x.id == macro_id), Macro(self.current_saveslot))

        self.MacroArea_Refresh()
        self.Pages_SetPage()
        self.Pages_RefreshAll()

    def MacrosTable_Refresh(self):
        """
        Refreshes the macros table on a left side of window.
        """

        self.button_AddMacros.setEnabled(self.current_saveslot.number > 0)
        self.button_DeleteMacros.setEnabled(self.current_saveslot.number > 0)

        # Clearing table.
        while self.tableWidget_Macros.rowCount():
            self.tableWidget_Macros.removeRow(0)

        macros = self.current_saveslot.macros
        for i, macro in enumerate(macros):

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
            self.tableWidget_Macros.setItem(i, 0, QTableWidgetItem(str(macro.id)))
            self.tableWidget_Macros.setItem(i, 1, QTableWidgetItem(macro.name))
            self.tableWidget_Macros.setItem(i, 2, QTableWidgetItem(hotkey))

    def lineEdit_MacroName_OnChange(self):
        """

        """
        self.current_macro.name = self.lineEdit_MacroName.text()
        self.MacrosTable_Refresh()

    def MacroType_OnChange(self):
        """

        """
        self.current_macro.type = self.comboBox_MacroType.currentText()

        # TODO: Не забыть стандартные значения забить при выборе типа
        # Set standard values.
        if self.current_macro.type == 'Equipment':
            pass

        if self.current_macro.type == 'Magic' \
                and self.current_macro.settings['magic']['spell_number'] == 0:
            if self.current_saveslot.spells:
                self.current_macro.settings['magic']['spell_number'] = 1

        if self.current_macro.type == 'Built-in' \
                and self.current_macro.settings['built-in']['macro_name'] == '':
            self.current_macro.settings['built-in']['macro_name'] = built_in_macros()[0]['name']

        self.hook_hotkeys()
        self.Pages_SetPage()
        self.Pages_RefreshAll()



    def OpenSaveFile_Click(self):
        """
        Shows a window for choosing Elden Ring savefile manually.
        """

        start_folder = str(Path.home())

        if self.savefile.location:
            start_folder = '\\'.join(self.savefile.location.split('\\')[:-1])
        elif os.path.exists(str(Path.home()) + '\\AppData\\Roaming\\EldenRing'):
            start_folder = str(Path.home()) + '\\AppData\\Roaming\\EldenRing'

        options = QFileDialog.Options()
        location, _ = QFileDialog.getOpenFileName(self,
                                                  "Choose your Elden Ring Save File",
                                                  start_folder,
                                                  "Elden Ring Save File (*.sl2)",
                                                  options=options)

        if location:
            self.savefile = SaveFile(location)
            self.savefile.fill_saveslots()
            self.savefile.read_game_controls()
            if self.savefile.saveslots:
                self.current_saveslot = self.savefile.saveslots[0]
                self.current_saveslot.get_equipment()
            else:
                self.current_saveslot = SaveSlot()
            self.current_macro = Macro(self.current_saveslot)
            self.hook_hotkeys()
            self.set_macros_settings_from_window()

            self.AvailableSpells_RefillTable()
            self.refresh_all()

    def Settings_Click(self):
        """

        :return:
        """
        if self.stackedWidget_Pages.currentIndex() != 5:
            self.stackedWidget_Pages.setCurrentIndex(5)
        else:
            self.Pages_SetPage()

    def AddMacro_Click(self):
        """

        :return:
        """

        new_macro = Macro(self.current_saveslot)
        new_macro.name = new_macro.name
        new_macro.id = new_macro.id
        new_macro.type = 'Equipment'

        self.current_saveslot.macros.append(new_macro)
        self.current_macro = new_macro

        self.set_macros_settings_from_window()
        self.refresh_all()

    def MacroKey_OnChange(self):
        """

        """

        current_text = self.comboBox_MacroKey.currentText()
        self.current_macro.hotkey = current_text

        self.hook_hotkeys()
        self.MacrosTable_Refresh()

    def MacroKeyCtrl_Click(self):
        """

        """


        checked = self.checkBox_MacroKeyCtrl.isChecked()
        self.current_macro.hotkey_ctrl = checked
        self.hook_hotkeys()
        self.MacrosTable_Refresh()

    def MacroKeyShift_Click(self):
        """

        """
        checked = self.checkBox_MacroKeyShift.isChecked()
        self.current_macro.hotkey_shift = checked
        self.hook_hotkeys()
        self.MacrosTable_Refresh()

    def MacroKeyAlt_Click(self):
        """

        """

        checked = self.checkBox_MacroKeyAlt.isChecked()
        self.current_macro.hotkey_alt = checked
        self.hook_hotkeys()
        self.MacrosTable_Refresh()

    def comboBox_InterruptKey_OnChange(self):
        """

        """

        current_text = self.comboBox_InterruptHotkey.currentText()
        self.interrupt_hotkey = current_text

        self.set_macros_settings_from_window()

    def InterruptKeyCtrl_Click(self):
        """

        """

        checked = self.checkBox_InterruptKeyCtrl.isChecked()
        self.interrupt_hotkey_ctrl = checked
        self.set_macros_settings_from_window()

    def InterruptKeyShift_Click(self):
        """

        """
        checked = self.checkBox_InterruptKeyShift.isChecked()
        self.interrupt_hotkey_shift = checked
        self.set_macros_settings_from_window()

    def InterruptKeyAlt_Click(self):
        """

        """

        checked = self.checkBox_InterruptKeyAlt.isChecked()
        self.interrupt_hotkey_alt = checked
        self.set_macros_settings_from_window()

    def DeleteMacros_Click(self):
        """

        :return:
        """

        self.current_saveslot.macros.remove(self.current_macro)
        self.current_macro = Macro(self.current_saveslot)
        self.hook_hotkeys()
        self.set_macros_settings_from_window()

        self.MacrosTable_Refresh()
        self.MacroArea_Refresh()
        self.Pages_SetPage()


    def refresh_all(self) -> None:
        """
        Refreshes all possible elements in window.
        """

        self.MacrosTable_Refresh()
        self.SaveSlotsComboBox_Refresh()
        self.MacroArea_Refresh()
        self.Pages_RefreshAll()
        self.Pages_SetPage()
        self.hook_hotkeys()

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

    def Pages_SetPage(self) -> None:
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

    def Pages_RefreshAll(self) -> None:
        """

        """
        self.Pages_Refresh_Equipment()
        self.Pages_Refresh_Magic()
        self.Pages_Refresh_Builtin()
        self.Pages_Refresh_DIY()
        self.Pages_Refresh_Settings()
        self.Pages_Refresh_Multiplayer()

    def Pages_Refresh_Equipment(self) -> None:
        """
        Refreshes elements on "Equipment" page.
        """

        pass

    def Pages_Refresh_Magic(self) -> None:
        """
        Refreshes elements on "Magic" page.
        """
        magic_settings = self.current_macro.settings['magic']

        self.checkBox_MagicInstantUseLeftHand.setChecked(magic_settings['instant_cast_left'])
        self.checkBox_MagicInstantUseRightHand.setChecked(magic_settings['instant_cast_right'])

        self.tableWidget_AvaiableMagic.clearSelection()
        if magic_settings['spell_number']:
            self.tableWidget_AvaiableMagic.selectRow(magic_settings['spell_number']-1)

    def AvaiableMagic_OnChange(self) -> None:
        """
        Changes setting in macro if another spell is chosen.
        """

        items = self.tableWidget_AvaiableMagic.selectedItems()
        if len(items):
            self.current_macro.settings['magic']['spell_number'] = items[0].row() - 1

    def MagicInstantUseRightHandCheck_OnChange(self) -> None:
        """
        Changes setting in macro if check "Right hand" on page "Magic" is changed.
        """
        self.current_macro.settings['magic']['instant_cast_right'] = \
            self.checkBox_MagicInstantUseRightHand.isChecked()

        if self.checkBox_MagicInstantUseRightHand.isChecked():
            self.checkBox_MagicInstantUseLeftHand.setChecked(False)
            self.current_macro.settings['magic']['instant_cast_left'] = False

        self.Pages_Refresh_Magic()

    def MagicInstantUseLeftHandCheck_OnChange(self) -> None:
        """
        Changes setting in macro if check "Left hand" on page "Magic" is changed.
        """
        self.current_macro.settings['magic']['instant_cast_left'] = \
            self.checkBox_MagicInstantUseLeftHand.isChecked()

        if self.checkBox_MagicInstantUseLeftHand.isChecked():
            self.checkBox_MagicInstantUseRightHand.setChecked(False)
            self.current_macro.settings['magic']['instant_cast_right'] = False

        self.Pages_Refresh_Magic()

    def AvailableSpells_RefillTable(self) -> None:
        """
        Refills spells on "Magic" page.
        """

        while self.tableWidget_AvaiableMagic.rowCount():
            self.tableWidget_AvaiableMagic.removeRow(0)

        for i, spell in enumerate(self.current_saveslot.spells):
            self.tableWidget_AvaiableMagic.insertRow(i)
            self.tableWidget_AvaiableMagic.setItem(i, 0, QTableWidgetItem(
                spell['name']))

    def Pages_Refresh_Builtin(self) -> None:
        """
        Refreshes elements on "Built-in" page.
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


    def Pages_Refresh_DIY(self) -> None:
        """
        Refreshes elements on "DIY" page.
        """

        self.textEdit_DIY.setText(self.current_macro.settings['diy']['macro'])

    def Pages_Refresh_Settings(self) -> None:
        """
        Refreshes elements on "Settings" page.
        """

        # Interrupt hotkey.
        self.comboBox_InterruptHotkey.setCurrentText(self.interrupt_hotkey)
        self.checkBox_InterruptKeyCtrl.setChecked(self.interrupt_hotkey_ctrl)
        self.checkBox_InterruptKeyShift.setChecked(self.interrupt_hotkey_shift)
        self.checkBox_InterruptKeyAlt.setChecked(self.interrupt_hotkey_alt)

        # Controls in Elden Ring.
        self.comboBox_ControlKeyRoll.setCurrentText(self.savefile.game_controls['roll'])
        self.comboBox_ControlKeyJump.setCurrentText(self.savefile.game_controls['jump'])
        self.comboBox_ControlKeyCrouch.setCurrentText(self.savefile.game_controls['crouch'])
        self.comboBox_ControlKeyResetCamera.setCurrentText(self.savefile.game_controls['reset_camera'])
        self.comboBox_ControlKeyAttack.setCurrentText(self.savefile.game_controls['attack'])
        self.comboBox_ControlKeyStrongAttack.setCurrentText(self.savefile.game_controls['strong_attack'])
        self.comboBox_ControlKeySkill.setCurrentText(self.savefile.game_controls['skill'])
        self.comboBox_ControlKeySwitchItem.setCurrentText(self.savefile.game_controls['switch_item'])
        self.comboBox_ControlKeySwitchSpell.setCurrentText(self.savefile.game_controls['switch_spell'])
        self.comboBox_ControlKeyGuard.setCurrentText(self.savefile.game_controls['guard'])
        self.comboBox_ControlKeyUseItem.setCurrentText(self.savefile.game_controls['use_item'])
        self.comboBox_ControlKeyUse.setCurrentText(self.savefile.game_controls['event_action'])

        # Standard pause time.
        self.spinBox_StandardPauseTime.setValue(self.standard_pause_time)

    def Pages_Refresh_Multiplayer(self) -> None:
        """
        Refreshes elements on "Multiplayer" page.
        """

        pass

    def BuiltInMacros_OnChange(self) -> None:
        """

        """

        items = self.tableWidget_BuiltInMacros.selectedItems()
        if len(items):
            self.current_macro.settings['built-in']['macro_name'] = items[0].text()
            self.Pages_Refresh_Builtin()

    def ControlKeys_OnChange(self):
        """
        Changes things after controls changed in "Settings" page.
        """

        self.savefile.game_controls['roll'] = self.comboBox_ControlKeyRoll.currentText().lower()
        self.savefile.game_controls['jump'] = self.comboBox_ControlKeyJump.currentText().lower()
        self.savefile.game_controls['crouch'] = self.comboBox_ControlKeyCrouch.currentText().lower()
        self.savefile.game_controls['reset_camera'] = self.comboBox_ControlKeyResetCamera.currentText().lower()
        self.savefile.game_controls['attack'] = self.comboBox_ControlKeyAttack.currentText().lower()
        self.savefile.game_controls['strong_attack'] = self.comboBox_ControlKeyStrongAttack.currentText().lower()
        self.savefile.game_controls['skill'] = self.comboBox_ControlKeySkill.currentText().lower()
        self.savefile.game_controls['switch_item'] = self.comboBox_ControlKeySwitchItem.currentText().lower()
        self.savefile.game_controls['switch_spell'] = self.comboBox_ControlKeySwitchSpell.currentText().lower()
        self.savefile.game_controls['guard'] = self.comboBox_ControlKeyGuard.currentText().lower()
        self.savefile.game_controls['use_item'] = self.comboBox_ControlKeyUseItem.currentText().lower()
        self.savefile.game_controls['event_action'] = self.comboBox_ControlKeyUse.currentText().lower()

        self.set_macros_settings_from_window()

    def textEdit_DIY_OnChange(self):
        """

        """

        self.current_macro.settings['diy']['macro'] = self.textEdit_DIY.toPlainText()

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def start_application():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_application()
