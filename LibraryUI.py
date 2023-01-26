#*********************************************************************
# content = LibraryUI for PANTRY Asset Library/Manager
#
# version = 1.0.0 
# date = 2022-12-04
#
# dependencies = Maya2020(currently)
#
# todos = Check PantryLibrary Module
#
# license = MIT
# author = Padmacumar Prabhaharan <padmacumar@gmail.com>
#*********************************************************************

import os
import sys

import PantryLibrary
reload(PantryLibrary)

from maya import cmds
from PySide2.QtWidgets import QMessageBox
from PySide2 import QtWidgets, QtCore, QtGui

#*********************************************************************
# CONSTANT VARIABLES

sys.path.append(r'E:\scripts')
PATH = r"E:\scripts\Pantry_AssetLibrary\PantryFiles"

#*********************************************************************
#Class
"""
Class for UI creation.
Inherits dictionary from PantryLibrary. 
For Maya.
"""
class AssetLibraryUI(QtWidgets.QDialog):

#****************************
    # Initiation
    def __init__(self):
        super(AssetLibraryUI, self).__init__()
        self.setWindowTitle('Pantry Manager')
        self.library = PantryLibrary.AssetLibrary()
        self.buildUI()


#****************************
    # Build UI layout
    def buildUI(self):
        layout = QtWidgets.QVBoxLayout(self)

        saveWidget = QtWidgets.QWidget()
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        layout.addWidget(saveWidget)

        self.saveNameField = QtWidgets.QLineEdit()
        saveLayout.addWidget(self.saveNameField)
        saveBtn = QtWidgets.QPushButton('Save')
        saveBtn.clicked.connect(self.save)
        saveLayout.addWidget(saveBtn)

        radioWidget = QtWidgets.QWidget()
        radioLayout = QtWidgets.QHBoxLayout(radioWidget)
        layout.addWidget(radioWidget)

        self.ma_radio = QtWidgets.QRadioButton('.ma')
        radioLayout.addWidget(self.ma_radio)
        self.ma_radio.setChecked(True)

        self.fbx_radio = QtWidgets.QRadioButton('.fbx')
        radioLayout.addWidget(self.fbx_radio)

        self.obj_radio = QtWidgets.QRadioButton('.obj')
        radioLayout.addWidget(self.obj_radio)

        size = 64

        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.listWidget.setIconSize(QtCore.QSize(size, size))
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidget.setGridSize(QtCore.QSize(size+12, size+12))
        layout.addWidget(self.listWidget)

        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        layout.addWidget(btnWidget)

        importBtn = QtWidgets.QPushButton('Import')
        importBtn.clicked.connect(self.load)
        btnLayout.addWidget(importBtn)

        refreshBtn = QtWidgets.QPushButton('Refresh')
        refreshBtn.clicked.connect(self.populate)
        btnLayout.addWidget(refreshBtn)

        closeBtn = QtWidgets.QPushButton('Close')
        closeBtn.clicked.connect(self.close)
        btnLayout.addWidget(closeBtn)

        self.populate()


#****************************
    # Load for .ma, .fbx, .obj with radio buttons
    def load(self):
        currentItem = self.listWidget.currentItem()

        if not currentItem:
            return

        name = currentItem.text()
        folder_path = os.path.join(PATH, name)

        if self.fbx_radio.isChecked():
            file_path = os.path.join(folder_path, '%s.fbx' % name)
        elif self.ma_radio.isChecked():
            file_path = os.path.join(folder_path, '%s.ma' % name)
        elif self.obj_radio.isChecked():
            file_path = os.path.join(folder_path, '%s.obj' % name)

        cmds.file(file_path, i=True, usingNamespaces=False)
        self.importsuccess_pop()
        print(file_path)


#****************************
    # Save for .ma, .fbx, .obj all together
    def save(self):
        name = self.saveNameField.text()

        if not name.strip():
            cmds.warning("You must give a name!")
            return

        filename = os.path.join(PATH, name)
        if os.path.exists(filename):
            self.exists_pop()
        else:
            self.library.save(name)
            self.populate()
            self.saveNameField.setText('')
            self.savesuccess_pop()


#****************************
    # Populate the List with files and icons
    def populate(self):
        self.listWidget.clear()

        if self.fbx_radio.isChecked():
            self.library.find_fbx()
            self.for_populate()
        elif self.ma_radio.isChecked():
            self.library.find_ma()
            self.for_populate()
        elif self.obj_radio.isChecked():
            self.library.find_obj()
            self.for_populate()

#***************
    # Extra function for populate to avoid repetition
    def for_populate(self):
        self.listWidget.clear()
        
        for name, path in self.library.items():
            item = QtWidgets.QListWidgetItem(name)
            self.listWidget.addItem(item)

            for thefile in path:
                if 'jpg' in thefile:
                    icon = QtGui.QIcon(thefile)
                    item.setIcon(icon)


#****************************
    #PopUps
    def exists_pop(self):
        btn_warn = QMessageBox.warning(self, 'Warning!', 'Name already exists! Give Another!')

    def savesuccess_pop(self):
        btn_savesuccess = QMessageBox.information(self, 'Saved', 'Files created successfully!')

    def importsuccess_pop(self):
        btn_importsuccess = QMessageBox.information(self, 'Imported', 'Files imported successfully!')
        

#****************************
# Function to display our UI
def showUI():
    ui = AssetLibraryUI()
    ui.show()
    return ui



