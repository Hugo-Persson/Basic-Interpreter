variables = {}
executionArrayGlobal={}
lineDeclaredListGlobal={}


def getValue(val):
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
    return

def handlePrint(execObj):
    print(getValue(execObj["value"]))
    return


def runInterpreter(executionArray, lineDeclaredList,start):
    executionArrayGlobal=executionArray
    lineDeclaredListGlobal=lineDeclaredList

    for index in range(start,len(executionArray)):

        i = executionArray[index]


        if(i["command"]=="GOTO"):
            lineNum = getValue(i["value"])
            runInterpreter(executionArray,lineDeclaredList,lineDeclaredList[str(lineNum)])
            return
        {
            "PRINT":handlePrint,
            "VARASSIGN":handleVariableAssignment
        }.get(i["command"],lambda:print("Error wrong command"))(i)

        