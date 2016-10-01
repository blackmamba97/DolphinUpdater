@echo off
pyinstaller -F --distpath "dist" --workpath "build" DolphinUpdater.spec
pause