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


def handlePrint(execObj):
    print(getValue(execObj["value"]))
    return

def generateNestedArray(depth):
    a=[]
    
    b=[]
    
    for i in range(0,depth-1): #becomes end index + 1 depth so this is two dimensional
        a.append(b)
        b=a
        a=[]
        
    print("ARRRRRR",b)
    return b

def getNestedArrayValue(depthArr, arr):
    arrValue = arr
    lastValue = None
    
        
    for i in depthArr:
        arrValue=arrValue[i]

    return arrValue


def handleArrInit(execObj):
    print("handleArR",execObj)
    variables[execObj["varId"]]={"arrDepth":execObj["arrDepth"],"array":True,"value":generateNestedArray(execObj["arrDepth"])}

def handleArrayAssignment(execObj):
    arrValue = variables[execObj["varId"]]["value"]
    arrDepth = execObj["arrDepth"]
    lastValue = arrDepth.pop(len(arrDepth)-1) #The array is reference based but not the value in the array
    for i in arrDepth: #[0,1,0]
        if(len(arrValue)-2<i):
            #expand array
            base  = arrValue[len(arrValue)-1] #I always have one element extra so I can copy it
            for n in range(len(arrValue),i+2):
                arrValue.append(base)
            arrValue=arrValue[i];
        else:
            arrValue=arrValue[i]
    if(lastValue>len(arrValue)-2):
        base= None
        if(len(arrDepth)+1!=variables[execObj["varId"]]["arrDepth"]): # I add one because the last elements has been popped
            base  = arrValue[len(arrValue)-1]
        for i in range(len(arrValue),lastValue+2):
            arrValue.append(base)
    print("ARRVALUE",arrValue) 
    arrValue[lastValue]=getValue(execObj["value"])

def handleVariableAssignment(execObj):
    print("EXEX",execObj)
    if(execObj["array"]):
        return handleArrayAssignment(execObj)

    variables[execObj["varId"]]= {"array":False, "value":getValue(execObj["value"])} 
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
            "VARASSIGN":handleVariableAssignment,
            "ARRINIT":handleArrInit,
            
        }.get(i["command"],lambda:print("Error wrong command"))(i)
    print("VARIABLES",variables)

        