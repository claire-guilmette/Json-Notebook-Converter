import json
from json import *
import sys
from pathlib import Path
import os



LOCAL_NOTEBOOK_FILE_ENDING = "_LOCAL.ipynb"
JSON_METADATA_FILE_ENDING = "_METADATA.json"

def exportMetadata(fileName, metadata):
    fileName = Path(fileName.split('.')[0] + JSON_METADATA_FILE_ENDING)
    print(f"Writing to {fileName}")
    try:
        with open(fileName, 'w', newline="\n") as file:
            json.dump(metadata, file, indent='\t', sort_keys=False)
    except:
        print("error writing metadata file")

def exportNotebook(fileName, cells):
    notebook = {"metadata":{}, "cells": cells}
    fileName = Path(fileName.split('.')[0] + LOCAL_NOTEBOOK_FILE_ENDING)
    print(f"Writing to {fileName}")
    try:
        with open(fileName, 'w', newline="\n") as file:
            json.dump(notebook, file, indent='\t', sort_keys=False)
    except:
        print("error writing to notebook file")

def exportJson(fileName, notebookJsonObject):
    fileName = Path(fileName)
    print(f"Writing to {fileName}")
    try:
        with open(fileName, 'w', newline="\n") as file:
            json.dump(notebookJsonObject, file, indent='\t', sort_keys=False)
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

def removeEmptyCellMetadata(cells):
    for cell in cells:
        if cell['metadata'] == {}:
            cell.pop('metadata')

def jsonifyNotebooks():
    print(f"searching for LOCAL files in {os.getcwd()}")

    allFiles = os.listdir('.')
    localFiles = [file for file in allFiles if file.endswith(LOCAL_NOTEBOOK_FILE_ENDING)]
    metaFiles = [file for file in allFiles if file.endswith(JSON_METADATA_FILE_ENDING)]

    print(localFiles)
    print(metaFiles)
    
    for localFile in localFiles:
        origFileName = localFile[0:-len(LOCAL_NOTEBOOK_FILE_ENDING)]
        metaFile = origFileName + JSON_METADATA_FILE_ENDING
        if metaFile in metaFiles:
            cellJson = importJson(localFile)['cells']
            metaJson = importJson(metaFile)
            removeEmptyCellMetadata(cellJson)
            metaJson['properties']['cells'] = cellJson
            exportJson(origFileName + ".json", metaJson)
        else:
            print(f"missing metadata file for {origFileName}")
            sys.exit()



i = 0
if len(sys.argv) == 1:
    print("USAGE: python notebookify.py [json_file_1] [json_file_2] ... ")
    print("Or to convert notebooks to json: python notebookify.py -j")
    print("\tThis will combine each file named *_LOCAL.ipynb with its _METADATA.json file")
elif (len(sys.argv) > 1 and sys.argv[1] == '-j'):
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
        
        if arg.endswith(JSON_METADATA_FILE_ENDING):
            print(f"METADATA file {arg} found. Skipping.")
            continue
        currentJson = importJson(arg)
        
        metadataObject = {'name': '', 'properties':{}}
        metadataObject['name'] = currentJson['name']
        cells = currentJson['properties'].pop('cells')
        for cell in cells:
            if 'metadata' not in cell.keys():
                cell['metadata'] = {}
        exportMetadata(arg, currentJson)
        exportNotebook(arg, cells)

        
    else:
        i += 1
