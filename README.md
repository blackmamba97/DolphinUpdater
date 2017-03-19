# Dolphin Updater

A script to update the [Dolphin emulator](https://github.com/dolphin-emu/dolphin) with ease in Windows.

The [official master builds](https://de.dolphin-emu.org/download/list/master/1/) and the [Ishiiruka](https://forums.dolphin-emu.org/Thread-unofficial-ishiiruka-dolphin-custom-version) fork are supported.

## Usage
Download the [executable](https://github.com/maxroehrl/DolphinUpdater/releases) and put in the directory where your `Dolphin.exe` is located.

You can also put the `DolphinUpdater.exe` anywhere and use the command-line.
```
DolphinUpdater.exe -p "path_to_dolphin_exe"
```

## Build the executable
You need Python 3 and pip to compile the code.

Download this repository and enter the following commands in the new directory.

Download the used libraries:
```
pip install bs4
pip install colorama
pip install PyInstaller
```

Run the build script:
```
build
```

The `DolphinUpdater.exe` is now located in the `dist` directory.
