@echo off

pip install --upgrade pip
pip install pyinstaller
pip install lxml
pip install os
pip install subprocess
pip install pyTelegramBotAPI

pyinstaller --onefile --windowed --icon "icon.ico"  "NetKey.py"

rmdir /s /q build

:cmd
pause null