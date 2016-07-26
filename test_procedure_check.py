import os # needed for the os.walk function
from Tkinter import Tk
from tkFileDialog import askdirectory

def find_tp_ln(fileName):
    """Method to find the line number of the location of 'REQUIREMENTS'
    in the text documents
    
    If no 'REQUIREMENTS' is found will return -1, otherwise returns line number
    """
    
    with open(fileName, 'r') as file:
        for num, line in enumerate(file, 1):
            if 'TEST PROCEDURE' in line:
                return num
        return -1 # if here no requirements found
    
    return

def check_tp(fileName, fullFileName):
    """Method to check the name of the TEST PROCEDURE.
    
    Will print out the name of any file whose TP does
    not match the name of the file.
    """
    
    # Create variable of proper tp name
    #correct_tp = str(fileName)
    index = 0
    correct_tp = ""
    name = fileName.strip().rstrip()
    for i in name:
        if index == 1:
            correct_tp += 'P'
        elif index == len(fileName) - 2:
            correct_tp += 's'
        else:
            correct_tp += i
        index += 1

    correct_tp = correct_tp.strip().rstrip()
    #correct_tp[1] = 'P'
    #correct_tp[len(correct_tp) - 2] = 's'
    #print('correct_tp %s' % correct_tp)
    
    
    line_number = find_tp_ln(fullFileName)
    if line_number == -1:
        print('ERROR: Could not find TEST PROCEDURE in ', fullFileName)
        return
    
    # Read in the file data
    with open(fullFileName, 'r') as fin:
        data = fin.read().splitlines(True)
        
    # Find the TP name
    tp_name = str(data[line_number]).strip().rstrip()
    #print('tp_name %s' % tp_name)

    # check if it matches
    if correct_tp != tp_name:
        print('\t%s' % tp_name)
        print('\t%s' % correct_tp)
        print('\n')

def main():
    """Script designed to replace the headers of Test Case documents"""
    
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
        
        print('Found directory: %s' % dirName)
        for file in fileList:
            if file.endswith('.txt') and file.startswith('TC'):
                check_tp(file, os.path.join(dirName, file)) # needs absolute path

                
if __name__ == '__main__':
    main()