import sys
import os
from pathlib import Path
from mainWindow import Ui_MainWindow
import PyQt5
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from macro import Macro, built_in_macros, available_hotkey_buttons
from savefile import SaveFile, SaveSlot
import keyboard

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

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
        self.recovery_hotkey: str = ''
        self.recovery_hotkey_ctrl: bool = False
        self.recovery_hotkey_shift: bool = False
        self.recovery_hotkey_alt: bool = False

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

        # Кружиться:
        # w_press60
        # a_press60
        # s_press60
        # d_press60
        # w_press60
        # pause20

        # teagabbing and alt+f4

    def set_macros_settings_from_window(self) -> None:
        """
        Sets macros settings with values from the window to all macros.
        """

        # TODO: разобраться с кнопкой прерывания-обновления, на некрасиво задается в любом случае переделать на хранение в сейв-файле
        recovery_hotkey = self.recovery_hotkey
        if self.recovery_hotkey_alt:
            recovery_hotkey = 'alt+' + recovery_hotkey
        if self.recovery_hotkey_shift:
            recovery_hotkey = 'shift+' + recovery_hotkey
        if self.recovery_hotkey_ctrl:
            recovery_hotkey = 'ctrl+' + recovery_hotkey

        for macro in self.current_saveslot.macros:
            macro.pause_time = self.standard_pause_time
            macro.recoveryed = False
            macro.recovery_hotkey = recovery_hotkey
            macro.saveslot = self.current_saveslot

    def hook_hotkeys(self):
        """

        """

        def hook_for_elden_ring(hotkey: str, func) -> None:
            """
            Hooks a hotkey in a way that fits to our process. 
            """

            # Need to rename some keys to make 'keyboard' eat it.
            hotkey = hotkey.replace('~', 'ё')
            if hotkey.lower().startswith('num') and len(hotkey) == 4:
                hotkey = hotkey[:3].lower() + ' ' + hotkey[-1]

            # As in Elden ring we can use hotkey during movement, we need to 
            # hook a hotkey to any movement combination we can have, including
            # all 8 directions and sprint button.
            # That's awful, but I don't know a method to do it differently.
            up = self.savefile.game_controls['move_up']
            down = self.savefile.game_controls['move_down']
            left = self.savefile.game_controls['move_left']
            right = self.savefile.game_controls['move_right']
            sprint = self.savefile.game_controls['roll']
            move_key_combos = ['', f'{up}+', f'{left}+', f'{down}+', f'{right}+',
                               f'{up}+{left}+', f'{up}+{right}+',
                               f'{right}+{down}+', f'{left}+{down}+',
                               f'{sprint}+{up}+', f'{sprint}+{down}+',
                               f'{sprint}+{right}+', f'{sprint}+{left}+',
                               f'{sprint}+{up}+{left}+', f'{sprint}+{up}+{right}+',
                               f'{sprint}+{right}+{down}+', f'{sprint}+{left}+{down}+']

            # TODO: все равно капризничает вот эта тильда, и с grave и с tilda
            # for move_key in move_key_combos:
            #     keyboard.add_hotkey(move_key + hotkey,
            #                         func,
            #                         suppress=True,
            #                         trigger_on_release=True)


        # Try block, because 'Keyboard' clearing methods can call
        # an unexpected exception if there's no assigned hotkeys.
        try:
            keyboard.remove_all_hotkeys()
            keyboard._hotkeys.clear()
        except:
            pass


        if self.recovery_hotkey:
            hook_for_elden_ring(self.recovery_hotkey, self.refresh_currents)

        for macro in self.current_saveslot.macros:

            hotkey_string = macro.hotkey_string()
            if not hotkey_string:
                continue

            # Condition helps to correct a situation when several hotkeys
            # are assign to one key.
            if hotkey_string not in keyboard._hotkeys:
                hook_for_elden_ring(hotkey_string, macro.execute)
                print(f'{macro.name} hooked to "{hotkey_string}"')

    def refresh_currents(self):
        """
        Refreshes current spells, weapons and equipment to 0.
        """

        # All cells in inventory.
        self.current_saveslot.current_weapon_right_1 = 0
        self.current_saveslot.current_weapon_right_2 = 0
        self.current_saveslot.current_weapon_right_3 = 0
        self.current_saveslot.current_weapon_left_1 = 0
        self.current_saveslot.current_weapon_left_2 = 0
        self.current_saveslot.current_weapon_left_3 = 0
        self.current_saveslot.current_armor_head = 0
        self.current_saveslot.current_armor_torso = 0
        self.current_saveslot.current_armor_hands = 0
        self.current_saveslot.current_armor_legs = 0
        self.current_saveslot.current_talisman_1 = 0
        self.current_saveslot.current_talisman_2 = 0
        self.current_saveslot.current_talisman_3 = 0
        self.current_saveslot.current_talisman_4 = 0

        # Magic.
        self.current_saveslot.current_spell = 0

        print('=' * 40)
        print('Currents were refreshed.')

    def init_ui(self):
        """

        """
        self.setupUi(self)  # automaticly generated code

        self.setFixedSize(1600, 890)
        self.setWindowTitle('ER - Melina\'s Fingers')
        self.button_OpenSaveFile.clicked.connect(self.OpenSaveFile_Click)
        self.button_SaveSettings.clicked.connect(self.save_settings)
        self.button_Settings.clicked.connect(self.Settings_Click)
        self.comboBox_SaveSlots.activated.connect(self.SaveSlots_OnChange)

        self.lineEdit_MacroName.editingFinished.connect(self.MacroName_OnChange)
        self.comboBox_MacroType.activated.connect(self.MacroType_OnChange)
        self.button_DeleteMacros.clicked.connect(self.DeleteMacros_Click)
        self.comboBox_MacroKey.activated.connect(self.MacroKey_OnChange)
        self.checkBox_MacroKeyCtrl.clicked.connect(self.MacroKeyCtrl_Click)
        self.checkBox_MacroKeyShift.clicked.connect(self.MacroKeyShift_Click)
        self.checkBox_MacroKeyAlt.clicked.connect(self.MacroKeyAlt_Click)
        for key in available_hotkey_buttons():
            self.comboBox_MacroKey.addItem(key)
            self.comboBox_RecoveryHotkey.addItem(key)

        # Macros table.
        self.tableWidget_Macros.itemSelectionChanged.connect(self.tableWidget_Macros_OnSelect)
        self.tableWidget_Macros.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_Macros.setColumnHidden(0, True)  # Hide ID column
        header = self.tableWidget_Macros.horizontalHeader()
        header = self.tableWidget_Macros.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.button_AddMacros.clicked.connect(self.AddMacro_Click)
        self.button_UpMacros.clicked.connect(self.UpMacro_Click)
        self.button_DownMacros.clicked.connect(self.DownMacro_Click)

        # Page "Equipment"

        # Page "Magic"
        self.tableWidget_AvaiableMagic.itemSelectionChanged.connect(self.AvaiableMagic_OnChange)
        self.tableWidget_AvaiableMagic.setEditTriggers(QTableWidget.NoEditTriggers)
        self.checkBox_MagicInstantUseLeftHand.clicked.connect(self.MagicInstantUseLeftHandCheck_OnChange)
        self.checkBox_MagicInstantUseRightHand.clicked.connect(self.MagicInstantUseRightHandCheck_OnChange)

        # Page "Built-in"
        self.tableWidget_BuiltInMacros.itemSelectionChanged.connect(self.BuiltInMacros_OnSelect)
        self.tableWidget_BuiltInMacros.setEditTriggers(QTableWidget.NoEditTriggers)

        # Page "DIY"
        self.textEdit_DIY.textChanged.connect(self.textEdit_DIY_OnChange)

        # Page "Settings"
        self.comboBox_RecoveryHotkey.activated.connect(self.RecoveryKey_OnChange)
        self.checkBox_RecoveryKeyCtrl.clicked.connect(self.RecoveryKeyCtrl_Click)
        self.checkBox_RecoveryKeyShift.clicked.connect(self.RecoveryKeyShift_Click)
        self.checkBox_RecoveryKeyAlt.clicked.connect(self.RecoveryKeyAlt_Click)

        self.comboBox_EquipmentSearchMode.activated.connect(self.SearchMode_OnChange)
        self.comboBox_MagicSearchMode.activated.connect(self.SearchMode_OnChange)

        self.comboBox_ControlKeyMove_Up.activated.connect(self.ControlKeys_OnChange)
        self.comboBox_ControlKeyMove_Down.activated.connect(self.ControlKeys_OnChange)
        self.comboBox_ControlKeyMove_Left.activated.connect(self.ControlKeys_OnChange)
        self.comboBox_ControlKeyMove_Right.activated.connect(self.ControlKeys_OnChange)
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
            self.comboBox_ControlKeyMove_Up.addItem(key)
            self.comboBox_ControlKeyMove_Down.addItem(key)
            self.comboBox_ControlKeyMove_Left.addItem(key)
            self.comboBox_ControlKeyMove_Right.addItem(key)
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

        if self.recovery_hotkey == '':
            self.recovery_hotkey = '~'

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

    def tableWidget_Macros_OnSelect(self):
        """

        :return:
        """
        items = self.tableWidget_Macros.selectedItems()
        if len(items):
            macro_id = int(self.tableWidget_Macros.item(items[0].row() , 0).text())
        else:
            return

        self.current_macro = next((x for x in self.current_saveslot.macros if x.id == macro_id), Macro(self.current_saveslot))

        self.MacroArea_Refresh()
        self.Pages_SetPage()
        self.Pages_RefreshAll()

    def MacrosTable_Refresh(self):
        """
        Refreshes the macros table on a left side of the window.
        """

        self.button_AddMacros.setEnabled(self.current_saveslot.number > 0)
        self.button_DeleteMacros.setEnabled(self.current_saveslot.number > 0)

        # Remembering current id for case of changing table.
        current_macro_id = self.current_macro.id

        # Clearing table.
        while self.tableWidget_Macros.rowCount():
            self.tableWidget_Macros.removeRow(0)

        macros = self.current_saveslot.macros
        for i, macro in enumerate(sorted(macros, key=lambda x: x.id)):

            hotkey_list = []
            hotkey = '...'
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

        # Selecting current macro.
        self.tableWidget_Macros.clearSelection()
        model = self.tableWidget_Macros.model()
        if current_macro_id:
            for row in range(model.rowCount()):
                index = model.index(row, 0)
                macro_id = int(model.data(index))
                if macro_id == current_macro_id:
                    self.tableWidget_Macros.selectRow(row)
                    break

    def MacroName_OnChange(self):
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

        self.set_macro_name_from_settings()
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

        """

        new_macro = Macro(self.current_saveslot)
        new_macro.name = new_macro.name
        new_macro.id = new_macro.id
        new_macro.type = 'Equipment'

        self.current_saveslot.macros.append(new_macro)
        self.current_macro = new_macro

        self.set_macros_settings_from_window()
        self.refresh_all()

    def UpMacro_Click(self):
        """
        Put a current macro to upper position by changing ID with neighbour
        macro. Then refreshes table.
        """

        if not self.current_macro.id:
            return

        # Looking for previous macro.
        previous_id = 0
        model = self.tableWidget_Macros.model()
        for row in range(model.rowCount()):
            index = model.index(row, 0)
            macro_id = int(model.data(index))
            if macro_id == self.current_macro.id:
                break
            else:
                previous_id = macro_id
        else:
            return

        previous_macro = next((x for x in self.current_saveslot.macros
                               if x.id == previous_id), None)

        if previous_macro is None:
            return

        # Changing id's
        self.current_macro.id, previous_macro.id = \
            previous_macro.id, self.current_macro.id

        self.MacrosTable_Refresh()

    def DownMacro_Click(self):
        """
        Put a current macro to a down position by changing ID with neighbour
        macro. Then refreshes table.
        """

        if not self.current_macro.id:
            return

        # Looking for previous macro.
        next_id = 0
        current_found = False
        model = self.tableWidget_Macros.model()
        for row in range(model.rowCount()):
            index = model.index(row, 0)
            macro_id = int(model.data(index))
            if current_found:
                next_id = macro_id
                break
            if macro_id == self.current_macro.id:
                current_found = True
        else:
            return

        next_macro = next((x for x in self.current_saveslot.macros
                               if x.id == next_id), None)

        if next_macro is None:
            return

        # Changing id's
        self.current_macro.id, next_macro.id = \
            next_macro.id, self.current_macro.id

        self.MacrosTable_Refresh()

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

    def RecoveryKey_OnChange(self):
        """

        """
        # TODO: отрефакторить в одну функцию: после изменения
        current_text = self.comboBox_RecoveryHotkey.currentText()
        self.recovery_hotkey = current_text

        self.set_macros_settings_from_window()

    def RecoveryKeyCtrl_Click(self):
        """

        """

        checked = self.checkBox_RecoveryKeyCtrl.isChecked()
        self.recovery_hotkey_ctrl = checked
        self.set_macros_settings_from_window()

    def RecoveryKeyShift_Click(self):
        """

        """
        checked = self.checkBox_RecoveryKeyShift.isChecked()
        self.recovery_hotkey_shift = checked
        self.set_macros_settings_from_window()

    def RecoveryKeyAlt_Click(self):
        """

        """

        checked = self.checkBox_RecoveryKeyAlt.isChecked()
        self.recovery_hotkey_alt = checked
        self.set_macros_settings_from_window()

    def SearchMode_OnChange(self):
        """
        Changes search mode settings after changing them in "Settings" page.
        """

        self.current_saveslot.search_mode_equipment = self.comboBox_EquipmentSearchMode.currentText()
        self.current_saveslot.search_mode_magic = self.comboBox_MagicSearchMode.currentText()

    def DeleteMacros_Click(self):
        """

        :return:
        """

        self.current_saveslot.macros.remove(self.current_macro)
        self.current_macro = Macro()
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
        if not len(items):
            return

        self.current_macro.settings['magic']['spell_number'] = items[0].row() + 1

        self.set_macro_name_from_settings()



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
        current_name_in_table = ''
        items = self.tableWidget_BuiltInMacros.selectedItems()
        if len(items):
            current_name_in_table = items[0].text()

        if current_builtin_macro_name:
            for i, item in enumerate(built_in_macros()):
                if item['name'] == current_builtin_macro_name\
                        and current_name_in_table != current_builtin_macro_name:
                    self.tableWidget_BuiltInMacros.clearSelection()
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

        # Recovery hotkey.
        self.comboBox_RecoveryHotkey.setCurrentText(self.recovery_hotkey)
        self.checkBox_RecoveryKeyCtrl.setChecked(self.recovery_hotkey_ctrl)
        self.checkBox_RecoveryKeyShift.setChecked(self.recovery_hotkey_shift)
        self.checkBox_RecoveryKeyAlt.setChecked(self.recovery_hotkey_alt)

        # Search modes.
        self.comboBox_EquipmentSearchMode.setCurrentText(self.current_saveslot.search_mode_equipment)
        self.comboBox_MagicSearchMode.setCurrentText(self.current_saveslot.search_mode_magic)

        # Controls in Elden Ring.
        self.comboBox_ControlKeyMove_Up.setCurrentText(self.savefile.game_controls['move_up'])
        self.comboBox_ControlKeyMove_Down.setCurrentText(self.savefile.game_controls['move_down'])
        self.comboBox_ControlKeyMove_Left.setCurrentText(self.savefile.game_controls['move_left'])
        self.comboBox_ControlKeyMove_Right.setCurrentText(self.savefile.game_controls['move_right'])
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

    def BuiltInMacros_OnSelect(self) -> None:
        """

        """

        items = self.tableWidget_BuiltInMacros.selectedItems()
        if not len(items):
            return

        built_in_macro_name = items[0].text()
        self.current_macro.settings['built-in']['macro_name'] = built_in_macro_name

        self.set_macro_name_from_settings()

        self.Pages_Refresh_Builtin()

    def ControlKeys_OnChange(self):
        """
        Changes things after controls changed in "Settings" page.
        """

        self.savefile.game_controls['move_up'] = self.comboBox_ControlKeyMove_Up.currentText().lower()
        self.savefile.game_controls['move_down'] = self.comboBox_ControlKeyMove_Down.currentText().lower()
        self.savefile.game_controls['move_left'] = self.comboBox_ControlKeyMove_Left.currentText().lower()
        self.savefile.game_controls['move_right'] = self.comboBox_ControlKeyMove_Right.currentText().lower()
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

    def set_macro_name_from_settings(self):
        """
        Sets macro name to something from page
        if macro name wasn't set by user.
        """

        if self.current_macro.type == 'Magic':

            items = self.tableWidget_AvaiableMagic.selectedItems()
            if not len(items):
                return

            spell_name = items[0].text()
            if self.current_macro.name == self.current_macro.standard_name() \
                    or any(x['name'] == self.current_macro.name for x in built_in_macros() + self.current_saveslot.spells):
                self.current_macro.name = spell_name
                self.MacroArea_Refresh()
                self.MacrosTable_Refresh()

            return

        if self.current_macro.type == 'Built-in':

            items = self.tableWidget_BuiltInMacros.selectedItems()
            if not len(items):
                return

            built_in_macro_name = items[0].text()
            if self.current_macro.name == self.current_macro.standard_name() \
                    or any(x['name'] == self.current_macro.name for x in built_in_macros() + self.current_saveslot.spells):
                self.current_macro.name = built_in_macro_name
                self.MacroArea_Refresh()
                self.MacrosTable_Refresh()

            return

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
