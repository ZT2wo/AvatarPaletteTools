<!-- ABOUT THE PROJECT -->
## About The Project

These sets of scripts allow modifying the character palettes for [Avatar Legends: The Fighting Game](https://store.steampowered.com/app/2424420/Avatar_Legends_The_Fighting_Game/) embedded in the ".pak" files locally.
These scripts scan the binary of the pak files for the offsets of the palette structures and overwrites them.

Here's why:
* The website [AVFG Palette Editor](https://avfg-palette-editor.up.railway.app/#) exists, however it's implementation of the runtime injection of palettes is not open source. The palette editor is great however and thus it's preset exporting is utilized here.
* It's implementation also requires overwriting the games pak files with a modified pak file when the game starts. This means having 2 of essentially the same pak files in storage. Sharing these modified pak files is also tricky since they include code unrelated to the palettes and thus constitute a grey area of piracy. Not that AVFG advocates this.
* This further implies that any updates to those pak files aside from their palettes would require you to rebuild all pak files using AVFG's exporter which is tedious and unideal in my opinion.

<!-- GETTING STARTED -->
## Getting Started

Make sure you have python installed and have downloaded the enabler, injector, and util scripts. Its not required as you can just make the folders yourself but for ease, also download the palettes_to_inject folder

### Installation

1. Place the 3 script files and the "palettes_to_inject" folder in the install directory of Avatar Legends

#### _Unlock all Hidden Palettes._
1. Double-click the enabler script and enter "y" at the prompt (This will enable all NON-DLC palettes)

If you've never installed python before this you may have to setup the file association

#### _Inject Palettes from local JSON_
1. Using [AVFG Palette Editor](https://avfg-palette-editor.up.railway.app/#) (Check it's tutorial), Make your custom palette and export the preset, not the pak. The buttons for this are below the materials.
2. Place your exported presets into the corresponding character folder in the "palettes_to_inject" folder.
3. Rename the preset to "color{the slot number of the palette}.json" i.e. "color3.json"
4. Double-click the injector script and enter "y" at the prompt

### You will need to re-run these whenever the game updates.



## TODO

- [ ] Add Local Editor