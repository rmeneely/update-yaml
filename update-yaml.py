#!/usr/bin/python3

# Modules
import sys, getopt
import re

# Syntax types
commentRegex = re.compile(r'^\s*#') # Comment
assignmentRegex = re.compile(r'^\s*\S*:\s*\S.*$')
contextRegex = re.compile(r'^\s*\S*:\s*$')
ListRegex = re.compile(r'^\s*-\s*\S*:\s*\S.*$')

# Global variables
Inputfile = ''       # YAML input file
Context = ''         # The current context (e.g. 'abc.def.ghi')
ContextLst = []      # The stack of contexts (e.g. ['abc', 'def', 'ghi']
ContextIndent = {}   # The indentation for a context (e.g. Context['abc.def.ghi'] = 2)
ContextValue = {}    # The current value of the context assignment
ContextNewValue = {} # The current value of the context assignment
Updated = False

def enterContext(contextName, indent):
    global Context
    global ContextLst
    ContextLst.append(contextName)
    Context = '.'.join(ContextLst)
    ContextIndent[Context] = indent
    return Context

def exitContext():
    global Context
    global ContextLst
    exitedContext = Context
    if len(ContextLst) > 0:
       ContextLst.pop()
       Context = '.'.join(ContextLst)
    return exitedContext

def get_lhs(theString, delimiter):
    theList = theString.split(delimiter)
    lhs = theList[0]
    lhs = lhs.strip()
    return lhs

def get_rhs(theString, delimiter):
    theList = theString.split(delimiter)
    rhs = theList[1]
    rhs = rhs.strip()
    return rhs

def setValue(context, value):
    global ContextValue
    ContextValue[context] = value

#def writeOutputs():
#    global Updated
#    updated = 'true' if Updated else 'false'
#    print("::set-output name=updated::{}".format(updated))

def main(argv):
    # Global variables
    global Inputfile
    global Context
    global ContextLst
    global ContextIndent
    global ContextValue
    global ContextNewValue
    global Updated
    
    # Default values
    Inputfile = 'values.yaml'
    Updated = False
    
    # Command line options
    try:
       opts, args = getopt.getopt(argv, "i:v:V:", ["infile=","var=","vars="])
    except getopt.GetoptError:
       print('update-yaml.py -i <inputfile> [-v <var=value>]')
       sys.exit(2)
    for opt, arg in opts:
        if opt in ('-v', "--var"): 
           lhs = get_lhs(arg,'=')
           rhs = get_rhs(arg,'=')
           ContextNewValue[lhs] = rhs
        elif opt in ('-V', "--vars"):
           varsLst = arg.split(',')
           for x in varsLst:
               lhs = get_lhs(x,'=')
               rhs = get_rhs(x,'=')
               ContextNewValue[lhs] = rhs
        elif opt in ("-i", "--ifile"):
           Inputfile = arg
    
    # Read yaml file
    infile = open(Inputfile, "r")
    contents = infile.read()
    infile.close
    yaml = contents.split('\n') # Create a list of the file contents
    yaml.pop() # Remove extra line created by split
    
    for line in yaml:
        indent = len(line) - len(line.lstrip())
        comment = commentRegex.search(line)
        assignment = assignmentRegex.search(line)
        newContext = contextRegex.search(line)
        list = ListRegex.search(line)
    
        # Exit contexts
        while (len(ContextLst) > 0) and (indent <= ContextIndent[Context]):
          exitContext()
    
        # Process this line
        if comment:
           print(line)
        elif assignment:
           lhs = get_lhs(assignment.group(), ':')
           rhs = get_rhs(assignment.group(), ':')
           Context = enterContext(lhs, indent)
           setValue(Context, rhs)
           if Context in ContextNewValue.keys():
              tmpLine = line.split(':')
              print("{}: {}".format(tmpLine[0], ContextNewValue[Context]))
              if rhs != ContextNewValue[Context]:
                 Updated = True
           else:
              print(line)
        elif newContext:
           lhs = get_lhs(newContext.group(), ':')
           Context = enterContext(lhs, indent)
           print(line)
        elif list:
           theItem = get_rhs(list.group(), '-')
           lhs = get_lhs(theItem, ':')
           rhs = get_rhs(theItem, ':')
           contextName = lhs + '.' + rhs
           Context = enterContext(contextName, indent)
           setValue(Context, rhs)
           if Context in ContextNewValue.keys():
              tmpLine = line.split(':')
              print("{}: {}".format(tmpLine[0], ContextNewValue[Context]))
              if rhs != ContextNewValue[Context]:
                 Updated = True
           else:
              print(line)
        else:
           print(line)
    
    # Write the output values
    #writeOutputs()

if __name__ == "__main__":
   main(sys.argv[1:])
