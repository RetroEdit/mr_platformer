# mr_platformer
Tools and info for Terry Cavanagh's 2023 game Mr. Platformer

## Save editor
Mr. Platformer has four different level types: forest, volcano, factory, and beach. The level types are randomly arranged on the map, but the level progression itself is not random. Each level type has a sequential progression of 10 primary layouts followed by one final layout.

The save editor provides some basic convenience arguments to modify the current level index for each type.

Requirements:
- Python 3.6 or later: if you don't have Python, you can look into installing it from here: https://www.python.org/downloads/
- Windows: the code is currently Windows-specific, but it could be easily modified to work on other platforms by adding alternate save paths.

### Usage examples
The save editor is currently a command-line program.

You'll want to open up your shell of choice and navigate to the directory where the script is downloaded. On Windows, the basic installed shells are Command Prompt and Powershell.

Display help:
```
python mr_platformer_saves.py -h
```

End any game processes, including those running in the background:
```
python mr_platformer_saves.py --closegame
```

End game processes and display the save file's contents:
```
python mr_platformer_saves.py --closegame --action read
```

End game processes and delete the save file:
```
python mr_platformer_saves.py --closegame --action reset
```

End game processes and overwrite the save file with one that starts with one forest level completed:
```
python mr_platformer_saves.py --closegame --action overwrite --forest 2
```

End game processes and overwrite the save file with one that starts at the first forest level with all other level types completed:
```
python mr_platformer_saves.py --closegame --action overwrite --forest 1 --autofill 11
```