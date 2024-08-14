# Json-Notebook-Converter (notebookify.py)

## Installation
Save the script to your machine. Then you can either add its folder to your path variable or create an alias to it for easy access.


## Usage

#### To convert synapse json files to python notebooks:

    python notebookify.py file1.json file2.json file3.json ...

or to convert all (could be a little excessive):

    python notebookify.py *.json


#### To convert all notebooks in the working dir back to json

    python notebookify.py -j
 
## Git Ignore
When converting to ipynb, the script saves the notebook as `[filename]_LOCAL.ipynb`, which you can then edit as needed.
If you wish you can include the following line in your `.gitignore` to easily keep these out of the repo:

    *_LOCAL.ipynb

## File Creation
This util is handy for existing files, but if you want to create a new notebook you should still create and commit it through the Synapse Analytics web editor. Synapse tracks a bunch of fields in the metadata that VSCode won't know to populate.