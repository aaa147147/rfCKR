REM pipenv lock
pyinstaller.exe -F -i .\GUI\ico\rfCKR.jpg --add-data "./GUI/ico/rfCKR.jpg;./GUI/ico" --add-data "./GUI/ico/SDMC_Logo.png;./GUI/ico" --upx-dir ./upx_cache .\rfCKR.py .\src\FileHandle.py .\src\iniHandle.py .\src\IQHandle.py .\src\litepoint.py .\src\SerialPort.py .\src\TestLoopMain.py .\src\ADBPort.py .\GUI\rfCKR_MainUI.py
