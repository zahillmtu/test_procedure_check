""" The following Python 2.7 script is designed to log the name
of any TC file whose TPs do not have an EXACT matching name.
The results are stored in 'results.log' in the same directory
as the script.

NOTE:
    Any Test Case file that does not have a 'TEST PROCEDURE' section
    will be treated as an error by this script. Anytime this is the case
    an ERROR is printed.

TO RUN:
    Run the script using python 2.7 and select the root directory from
    the pop up window. The script will traverse the root directory and
    all subdirectories beneath it to check the TP file names.
"""

__author__  = "Zachary Hill"
__email__   = "zachary.hill@psware.com"

import os # needed for the os.walk function
from Tkinter import Tk
from tkFileDialog import askdirectory
import re
import sys

FILECOUNT = 0
ERRORCOUNT = 0

def find_tp_ln(fileName):
    """Method to find the line number of the location of 'TEST PROCEDURE'
    in the text documents
    
    If no 'TEST PROCEDURE' is found will return -1, otherwise returns line number
    """
    
    with open(fileName, 'r') as file:
        for num, line in enumerate(file, 1):
            if 'TEST PROCEDURE' in line:
                return num
        return -1 # if here no TEST PROCEDURE found
    
    return

def check_tp(fileName, fullFileName):
    """Method to check the name of the TEST PROCEDURE.
    
    Will print out the name of any file whose TP does
    not match the name of the file.
    """
    
    global ERRORCOUNT
    
    # Create variable of proper tp name
    index = 0
    correct_tp = ""
    tp_doc_name = ""
    name = fileName.strip().rstrip()
    for i in name:
        if index == 1:
            correct_tp += 'P'
        elif index == len(fileName) - 2:
            correct_tp += 's'
        else:
            correct_tp += i
        index += 1

    correct_tp = str(correct_tp).strip().rstrip()
    correct_doc_tp = correct_tp[:len(correct_tp) - 3] + 'doc'
    #print('DOC THING %s' % correct_doc_tp)
    
    line_number = find_tp_ln(fullFileName)
    #print(fullFileName)
    if line_number == -1:
        print('\tERROR: Could not find TEST PROCEDURE in %s' % fullFileName)
        print('\n')
        ERRORCOUNT += 1
        return
    
    # Read in the file data
    with open(fullFileName, 'r') as fin:
        data = fin.read().splitlines(True)
        
    # Find the TP name
    #tp_name = str(data[line_number]).strip().rstrip()
    m1 = re.search('TP\w+\.tst', str(data[line_number]).strip().rstrip())
    if m1:
        tp_name = m1.group(0)
    else:
        print('\t%s' % fileName)
        ERRORCOUNT += 1
        return
    
    # Find the .doc file if there is one
    m1 = re.search('TP\w+.doc', str(data[line_number + 1]).strip().rstrip())    
    if m1:
        tp_doc_name = m1.group(0)
    else:
        tp_doc_name = ""

    # check if it matches
    if correct_tp != tp_name:
        ERRORCOUNT += 1
        print('\t%s' % fileName)
        
    if tp_doc_name != "":
        # check if doc matches
        if correct_doc_tp != tp_doc_name:
            print('\t%s' % fileName)


def main():
    """Script designed to replace the headers of Test Case documents"""
    
    global FILECOUNT, ERRORCOUNT
    
    # Redirect output to a file
    sys.stdout = open('./results.log', "w")
    
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    rootDir = askdirectory() # show an "Open" dialog box and return the path to the selected file
    print('Head of tree travesal selected %s' % rootDir)
    
    print('Listing files whose TPs do not match the file name...')
    print('\n')
    
    # Traverse the tree
    for dirName, subdirList, fileList in os.walk(rootDir):
        # Ignore hidden files and directories
        fileList = [f for f in fileList if not f[0] == '.']
        subdirList[:] = [d for d in subdirList if not d[0] == '.']
        print('\n')
        print('Found directory: %s' % dirName)
        for file in fileList:
            if file.endswith('.txt') and file.startswith('TC'):
                FILECOUNT += 1
                check_tp(file, os.path.join(dirName, file)) # needs absolute path

    print('\n')
    print('Total number of TC file checked: %d' % FILECOUNT)
    print('Total number of TC files with wrong TP names: %d' % ERRORCOUNT)
    if FILECOUNT != 0:
        print('Percent Error: %d%%' % (((1.0 * ERRORCOUNT) / FILECOUNT) * 100))    
                
if __name__ == '__main__':
    main()