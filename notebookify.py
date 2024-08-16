import json
from json import *
import sys
from pathlib import Path
import os



LOCAL_NOTEBOOK_FILE_ENDING = "_LOCAL.ipynb"

def exportNotebook(fileName, notebookJson):
    fileName = Path(fileName.split('.')[0] + LOCAL_NOTEBOOK_FILE_ENDING)
    print(f"Writing to {fileName}")
    try:
        with open(fileName, 'w', newline="\n") as file:
            json.dump(notebookJson, file, indent='\t', sort_keys=False)
    except:
        print("error writing to notebook file")

def exportJson(fileName, synapseJson):
    fileName = Path(fileName)
    print(f"Writing to {fileName}")
    try:
        with open(fileName, 'w', newline="\n") as file:
            json.dump(synapseJson, file, indent='\t', sort_keys=False)
    except:
        print(f"error writing to json file {fileName}")

def importJson(fileName):
    try:
        with open(fileName, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File '{fileName}' not found. Please provide the correct file path.")
        sys.exit()


def jsonifyNotebooks():
    print(f"searching for LOCAL files in {os.getcwd()}")

    allFiles = os.listdir('.')
    localFiles = [file for file in allFiles if file.endswith(LOCAL_NOTEBOOK_FILE_ENDING)]

    for localFile in localFiles:
        origFileName = localFile[0:-len(LOCAL_NOTEBOOK_FILE_ENDING)]
        
        notebook = importJson(localFile)
        #Everything but the name goes in the 'properties' object, so pop name off here if exists.
        name = ''
        print(notebook.keys())
        if 'name' in notebook.keys():
            name = notebook.pop('name')
        else:
            name = origFileName
            print(f'No name field for {localFile}. Generating from filename.')
        
        #remove empty metadata fields to minimize diff noise
        for cell in notebook['cells']:
            if cell['metadata'] == {}:
                cell.pop('metadata')
        jsonObject = {'name': name,
                      'properties': notebook}
        exportJson(origFileName + ".json", jsonObject)

i = 0
if len(sys.argv) == 1:
    print("USAGE: python notebookify.py [json_file_1] [json_file_2] ... ")
    print("Or to convert notebooks to json: python notebookify.py -j")
elif (len(sys.argv) > 1 and sys.argv[1].startswith('-j')):
    jsonifyNotebooks()
    sys.exit()
    
workingDirFiles = os.listdir('.')
for arg in sys.argv:
    if i > 0: 
        existingLocalNotebook = arg.split('.')[0] + LOCAL_NOTEBOOK_FILE_ENDING
        if existingLocalNotebook in workingDirFiles:
            print(f"Warning! This process will replace {existingLocalNotebook}.")
            goOn = input("Do you wish to continue? (y/n):")
            #anything but yes we skip this file.
            if not goOn.lower().startswith('y'):
                continue #ironically, continuing the loop means skipping the file.
        
        currentJson = importJson(arg)
        
        notebookObject = currentJson['properties']
        notebookObject['name'] = currentJson['name']
        for cell in notebookObject['cells']:
            if 'metadata' not in cell.keys():
                cell['metadata'] = {}
        exportNotebook(arg, notebookObject)

        
    else:
        i += 1
