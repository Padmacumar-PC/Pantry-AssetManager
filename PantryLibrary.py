#*********************************************************************
# content = PANTRY Asset Library/Manager
#
# version = 1.0.0 
# date = 2022-12-04
#
# dependencies = Maya2020(currently)
#
# todos = Import or load options for Nuke (fbx and obj)
#         Manual choice options for saving.
#         Make tool for newer Maya version (python 3.7+)
#         Extented the tool for other dcc pakages
#         Stress test required for some bugs fixes and to be noted 
#
# license = MIT
# author = Padmacumar Prabhaharan <padmacumar@gmail.com>
#*********************************************************************

import os
from maya import cmds

#*********************************************************************
# CONSTANT VARIABLES

PATH = r"E:\scripts\Pantry_AssetLibrary"

DIRECTORY = os.path.join(PATH, 'PantryFiles')

#*********************************************************************
# Create DIRECTORY if it doesn't already exist.

def create_dir(directory=DIRECTORY):
	if not os.path.exists(directory):
		os.mkdir(directory)

#*********************************************************************
#Class
"""
Class for dictionary creation.
Used for Inheritance into UI class. 
For Maya.
"""
class AssetLibrary(dict):

#****************************
    # Save
    """
    Currently saves .ma, .fbx, .obj all at once.
    Also triggers screenshot function and saves in same location.
    """
    def save(self, name, screenshot=True, directory=DIRECTORY):
        create_dir(directory)
        filefolder = os.path.join(directory, name)
        os.mkdir(filefolder)
        filename = os.path.join(filefolder, name)

        def exportformats():
            cmds.file(filename, force=True, exportSelected=True, type = 'mayaAscii')
            cmds.file(filename, force=True, exportSelected=True, type = 'FBX export')
            cmds.file(filename, force=True, exportSelected=True, type = 'OBJexport')

        if cmds.ls(selection=True):
            exportformats()
        else:
            cmds.select(all=True)
            exportformats()

        if screenshot:
            self.savescreenshot(name)


#****************************       
    # Find .ma files
    def find_ma(self, directory=DIRECTORY):
        self.clear()

        if not os.path.exists(directory):
            return

        for folder in os.listdir(directory):
            subfolder = os.path.join(directory, folder)
            files = os.listdir(subfolder)

            mayafiles = []

            for thefile in files:
                if thefile.endswith('.ma'):
                    mayafiles.append(thefile)
                    
                    for mafile in mayafiles:
                        ma_name, ext = os.path.splitext(mafile)
                        ma_filepath = os.path.join(subfolder, mafile)

                        screenshot = '%s.jpg' % ma_name

                        if screenshot in files:
                            img_filepath = os.path.join(subfolder, screenshot)

                            self[ma_name] = ma_filepath, img_filepath


#****************************       
    # Find .obj files
    def find_obj(self, directory=DIRECTORY):
        self.clear()

        if not os.path.exists(directory):
            return

        for folder in os.listdir(directory):
            subfolder = os.path.join(directory, folder)

            files = os.listdir(subfolder)

            objfiles = []

            for thefile in files:
                if thefile.endswith('.obj'):
                    objfiles.append(thefile)
                    
                    for objfile in objfiles:
                        obj_name, ext = os.path.splitext(objfile)
                        obj_filepath = os.path.join(subfolder, objfile)

                        screenshot = '%s.jpg' % obj_name

                        if screenshot in files:
                            img_filepath = os.path.join(subfolder, screenshot)

                            self[obj_name] = obj_filepath, img_filepath


#****************************       
    # Find .fbx files
    def find_fbx(self, directory=DIRECTORY):
        self.clear()

        if not os.path.exists(directory):
            return

        for folder in os.listdir(directory):
            subfolder = os.path.join(directory, folder)
            files = os.listdir(subfolder)

            fbxfiles = []

            for thefile in files:
                if thefile.endswith('.fbx'):
                    fbxfiles.append(thefile)
                    
                    for fbxfile in fbxfiles:
                        fbx_name, ext = os.path.splitext(fbxfile)
                        fbx_filepath = os.path.join(subfolder, fbxfile)

                        screenshot = '%s.jpg' % fbx_name

                        if screenshot in files:
                            img_filepath = os.path.join(subfolder, screenshot)

                            self[fbx_name] = fbx_filepath, img_filepath


#****************************
    # Create screenshot
    def savescreenshot(self, name, directory=DIRECTORY):
        folder = os.path.join(directory, name)
        imgfile = os.path.join(folder, '%s.jpg' % name)

        cmds.viewFit()
        cmds.select(clear=True)
        cmds.setAttr("defaultRenderGlobals.imageFormat", 8)
        cmds.playblast(completeFilename=imgfile, forceOverwrite=True, format='image', width=300, height=300,
                        showOrnaments=False, startTime=1, endTime=1, viewer=False)

        return imgfile