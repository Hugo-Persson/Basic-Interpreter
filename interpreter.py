variables = {}
executionArrayGlobal={}
lineDeclaredListGlobal={}


def getValue(val):
    print("VAL",val)
    value = None
    if(val["type"]=="INT"):
        value=int(val["value"])
    elif(val["type"]=="FLOAT"):
        value=float(val["value"])
    elif(val["type"]=="STRING"):
        value=val["value"]
    elif(val["type"]=="VAR"):
        value=variables[val["varId"]]
    else:
        print("Value wrong type, parser error")
    return value


def handleVariableAssignment(execObj):
    variables[execObj["varId"]]=getValue(execObj["value"])
    print("VARS",variables)
    return

def handlePrint(execObj):
    print(getValue(execObj["value"]))
    return

def runInterpreter(executionArray, lineDeclaredList):
    executionArrayGlobal=executionArray
    lineDeclaredListGlobal=lineDeclaredList
    for i in executionArray:
        print(i)
        {
            "PRINT":handlePrint,
            "VARASSIGN":handleVariableAssignment
        }.get(i["command"],lambda:print("Error wrong command"))(i)