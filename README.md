# Dolphin Updater

A script to update the [Dolphin emulator](https://github.com/dolphin-emu/dolphin) with ease in Windows.
The [official master builds](https://de.dolphin-emu.org/download/list/master/1/) and the [Ishiiruka](https://forums.dolphin-emu.org/Thread-unofficial-ishiiruka-dolphin-custom-version) fork are supported.

---

##Usage
Download the [executable](https://github.com/blackmamba97/DolphinUpdater/releases/download/1.0.0/DolphinUpdater_1.0.0.zip) and put in the directory where your <code>Dolphin.exe</code> is located.

You can also put the <code>DolphinUpdater.exe</code> anywhere and use the command-line</code>.

<code>DolphinUpdater.exe -p "path_to_dolphin_exe"</code>

---

##Build the executable
You need Python 3 and pip to compile the code.
Download this repository and enter the following commands in the new directory.

Download the used libraries:
<code>pip install bs4</code>
<code>pip install colorama</code>
<code>pip install PyInstaller</code>

Run the build script:
<code>build</code>

The <code>DolphinUpdater.exe</code> is now located in the <code>dist</code> directory.