import sys
import random
from evalins import parse

executionFlow = {}

def parseExecution(code):
    arr = code.split("<code object")[1].strip(" ").split("at 0x")
    func = arr[0].strip(" ")
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
        print("[*] Starting trace of: "+str(func))
        sys.settrace(traceit)
        func()
        print("[*] Trace Complete.")
        print("[*] Results: "+str(executionFlow))
        return 
    return do

'''
Example function we set up a trace on using a python decorator.

Scenario, we detected that there is a vulnerability in the library: "evalins.py" use of unsanitized input
can lead to remote code execution. 

However in our python program we don't know if the funtion "parse" is used. Note: Assume that we are blind
as a bat or want to efficienctly comb the entire code set without having to manually search it.

'''

@vulntrace
def main():
    parse("print(\"pwned\")")

main()