import sys
import random

executionFlow = {}

def parseExecution(code):
    arr = code.split("<code object")[1].strip(" ").split("at 0x")
    func = arr[0]
    file = arr[1].split("file")[1].split(",")[0].strip(" ")
    line = arr[1].split("file")[1].split(",")[1].split(">")[0].strip(" ")
    executionFlow[func] = {
        "file":file,
        "line":line
    }

def traceit(frame, event, arg):
    if event == "line":
       parseExecution(str(frame.f_code))
    return traceit

def vulntrace(func):
    def do():
        sys.settrace(traceit)
        return func()
    return do

'''
Example function we set up a trace on using a python decorator.
'''

@vulntrace
def main():
    print("In main")
    for i in range(5):
        print(i, random.randrange(0, 10))
    print ("Done.")
    print(executionFlow)

main()