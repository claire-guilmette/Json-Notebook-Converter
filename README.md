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
When converting to ipynb, the script saves the notebook as `[filename]_LOCAL.ipynb`, which you can then edit as needed. The script saves azure's unused json fields as a separate json file to be reattached when you're done editing. 
You can include the following lines in your `.gitignore` to easily keep these out of the repo:

    *_LOCAL.ipynb
    *_METADATA.json

