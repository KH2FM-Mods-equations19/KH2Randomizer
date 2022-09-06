# PC New Setup Guide

## Heads up!
* Feel free to go to the [discord server](https://discord.gg/vKhdwNAmzE) for help with the setup, there is a dedicated help channel where you can find people to help you, if you're facing any difficulties. (P.S. Please be polite)
* You must run the game once before you start the guide. Otherwise it may not boot up correctly after the randomizer is installed.
* VERIFY GAME FILES through the Epic Games Launcher for Kingdom Hearts 1.5 + 2.5 remix v1.0.0.8_WW (pirated copies are not supported, it is strongly recommended you buy and install the game directly from the Epic Game Store).

## Resources Needed:
* [OpenKH Mod Manager](https://github.com/shananas/OpenKh/releases/download/release-372-KH2Rando/openkh-modmanager.zip)
* [Seed Generator](https://github.com/tommadness/KH2Randomizer/releases/latest/download/Kingdom.Hearts.II.Final.Mix.Randomizer.zip)
* [.NET6 Desktop Runtime](https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/runtime-desktop-6.0.7-windows-x64-installer)

## Installing OpenKh and Seed Generator
1. Install .NET6 Runtime by running `windowsdesktop-runtime-6.0.7-win-x64.exe`
2. Create a KH2 Rando Folder On Your Computer (Recommended *not* to be in your games installation folder)
3. Extract OpenKH to this folder
4. Extract Seed Generator to this Folder

![Rando Folder](../images/Panacea-ModLoader/KH2%20Rando%20Folder.png)

## How to Setup The Mod Manager:
1. Run the **"OpenKh.Tools.ModsManager.exe"** in the OpenKH folder 
	- The Setup Wizard will open automatically, click **"Next"** to start.
2. Change game edition to **"PC Release Via Epic Games Store"**
3. Then click the folder icon and navigate to your KH1.5_2.5 installation folder (The default is "C:\Program Files\Epic Games\KH_1.5_2.5" but this may differ from your own)

![Setup Wizard-Game Edition](../images/Panacea-ModLoader/Game%20Edition%20Window.png)

4. Click the **"Install OpenKH Panacea"** Button. This will install the mod loader to your game installation folder

![Panacea Wizard Window](../images/Panacea-ModLoader/Panacea%20Install%20Window.png)

5. If you want Mod Manager to bypass the Epic Games launcher check the **"Bypass the launcher"** check box. YOU HAVE TO RUN KH2 THROUGH THE MOD MANAGER USING THE "**RUN"** COMMAND IF YOU CHOOSE THIS OPTION. YOU CANNOT RUN KH2 THROUGH THE REGULAR LAUNCHER WHILE THIS OPTION IS ENABLED.
	* *You will need to input your Epic Games user id, which can be found using the link below the text box*

![Bypass Launcher](../images/Panacea-ModLoader/Bypass%20Launcher.png)

6. Keep the extraction folder location as defaulted by the wizard, and click on the **"extract game data"** button. You will need to wait a few minutes for the process to complete.

![Extraction Window](../images/Panacea-ModLoader/Extraction%20Window.png)

## Garden of Assemblage Mod:
1. Click **"Mods"** in the top left

![Install New Mod](../images/Panacea-ModLoader/Install%20New%20Mod.png)

2. In the **"Add a new mod from Github"** section, type in the account name and mod name.
	- Type **"KH2FM-Mods-Num/GoA-ROM-Edition"** into the text box and click on **"Install"** in the bottom right

![Install GoA ROM](../images/Panacea-ModLoader/Install%20GoA%20ROM.png)

3. To enable the mod, be sure to click the checkbox next to the newly added mod in the list

![Enable GoA ROM](../images/Panacea-ModLoader/Enable_GoA_ROM.png)

4. Then click **"Game"** and **"Build"**, then **"Build Only"**

![Build Only](../images/Panacea-ModLoader/Build%20Only.png)

* *Note: Every time you add a new mod to the list you will need to **"Build"** again, or it wont show up in game*

## Lua Backend Installation:
1. Open the seed Generator Program `KH2 Randomizer.exe`
2. In the top left click on the **"Configure"** tab, then click on **"Luabackend Hook Setup (PC Only)**

![Backend Hook Setup 1](../images/Panacea-ModLoader/Backend%20Hook%20Setup%201.png)

3. In this new window click on **"browse"** next to the OpenKh Location, and browse to your openkh folder, then click **"select folder"**
4. For **"Mod mode"**, click the drop down and select **"Panacea/Mod Loader"**
5. Click on **"Check configuration"**
	* *The status messages below should say "Not Found"*

6. Now click on the **"Download/Install/Configure"** button in the bottom left. You can now close this window.

![Backend Hook Setup 2](../images/Panacea-ModLoader/LuaBackend%20Hook%20Setup%202.gif)

## Installing a new seed to play:
1. Choose your seed settings in the generator window and then click on **"Generate Seed"** in the bottom right.

*If you choose settings that may not act the same between the PCSX2 and PC version, the button will separate between PC and PCSX2, be sure to click the right one if it does so.*

2. This will open up a window to save the seed as a zip file. Save it anywhere that works for you (I like to place it in the same folder as the generator)
3. Once saved, open up the mod manager and click on **"Mods"**, then **"Install a New Mod"**
4. This time click on **"Select and Install Mod Archive"**, navigate to your new seed zip file and click **"Open"**
5. Be sure to click on the check box next to the seed, then click on **"Build"** and **"Build Only"** to enable the mod in game. Note the 4 buttons to the right of the mod list. The First button lets you move a mod up the list, the second moves them down the list. The Green '+' icon is a shortcut to install a new mod, while the Red "-" icon is a shortcut to deleting a mod.

![Install New Seed](../images/Panacea-ModLoader/Install%20New%20Seed.gif)

### *Note: It is very important that the seed is always ABOVE the GoA ROM mod in the list. The Randomizer will not work otherwise.*

*Editors note: I heavily recommend you install these two mods to help provide a better experience when playing rando -*

* **KH2FM-Mods-equations19/auto-save** - This mod auto saves the game for you as you enter rooms. Be sure to make at least 1 regular save in game, then if you ever crash or your game closes unexpectedly, just hold the **SELECT** button while loading a save, and the auto-save will be loaded instead.
* **KH2FM-Mods-equations19/soft-reset** - Hold **L1+L2+R1+R2+Start** at the same time to immediately reset the game to the start screen. Very useful if you accidentally softlock in boss/enemy rando, or just to restart the game faster!


# *You are now ready to play a KH2 Rando Seed! Run the game from the epic games launcher and have fun!*