# Pantry-AssetManager


This is Pantry Manager Tool v1.0.

If you wanna use it, read the script content and update it to your own folder path.

In Maya 2020 (current working dcc for this script) write the following script and save it in a shelf ( as python script ).

import sys

sys.path.append('\scriptfolder')

from Pantry_AssetLibrary import LibraryUI

reload(LibraryUI)

ui = LibraryUI.showUI()
