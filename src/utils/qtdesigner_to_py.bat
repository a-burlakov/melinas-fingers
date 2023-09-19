pyuic5 -x mainWindow.ui -o mainWindow.py 
pyrcc5 -o ui_rc.py ui.qrc

powershell -Command "(gc mainWindow.py) -replace 'import ui_rc', 'import src.utils.ui_rc' | Out-File -encoding ASCII mainWindow.py"

exit